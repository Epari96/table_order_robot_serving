#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, sqlite3
from datetime import datetime
from collections import defaultdict
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTextEdit, QPushButton, QButtonGroup

def _jloads(s):
    try: return json.loads(s) if s else {}
    except Exception: return s
def _jdumps(o):
    try: return json.dumps(o, ensure_ascii=False, indent=2)
    except Exception: return str(o)
def _merge_item_dicts(items_list):
    """[{"짜장면":1}, {"짬뽕":2}, ...] 같은 리스트를 합산 dict로"""
    merged = {}
    for it in items_list:
        if isinstance(it, dict):
            for k, v in it.items():
                if isinstance(v, (int, float)):
                    merged[k] = merged.get(k, 0) + int(v)
    return merged
def _items_to_text(items):
    """{"짜장면":2,"짬뽕":1} -> '짜장면 2개\n짬뽕 1개'"""
    if not isinstance(items, dict) or not items:
        return "(주문 내역 없음)"
    lines = [f"{name} {int(qty)}개" for name, qty in items.items() if isinstance(qty, (int, float)) and qty > 0]
    return "\n".join(lines) if lines else "(주문 내역 없음)"


class PosGuiWidget(QtWidgets.QMainWindow):
    requestNavGoal   = QtCore.pyqtSignal(str, float, float, float)
    requestCancel    = QtCore.pyqtSignal()
    requestZeroTwist = QtCore.pyqtSignal(float)
    orderDecision    = QtCore.pyqtSignal(str, bool)

    def __init__(self, ui_path: str, nav_points: dict, db_path: str):
        super().__init__()
        if not os.path.exists(ui_path):
            QMessageBox.critical(self, "UI Error", f"UI file not found: {ui_path}"); raise SystemExit(1)
        self.nav_points, self.db_path = nav_points, db_path
        self.ui = uic.loadUi(ui_path, self)

        # 필수 위젯
        g = lambda t,n: self.findChild(t, n)
        self.btnRobot1=g(QtWidgets.QPushButton,"btnRobot1"); self.btnRobot2=g(QtWidgets.QPushButton,"btnRobot2")
        self.btnCallRobot=g(QtWidgets.QPushButton,"btnCallRobot"); self.btnGoCharge=g(QtWidgets.QPushButton,"btnGoCharge")
        self.btnEStop=g(QtWidgets.QPushButton,"btnEStop"); self.btnPayment=g(QtWidgets.QPushButton,"btnPayment")
        self.btnSales=g(QtWidgets.QPushButton,"btnSales"); self.txtOrderLog=g(QtWidgets.QTextEdit,"txtOrderLog")

        # 좌/우 테이블 버튼
        all_btns = self.findChildren(QtWidgets.QPushButton)
        self.ctrl_table_buttons   = sorted([b for b in all_btns if b.objectName().startswith("btnCtrlTable")], key=lambda b:int(b.objectName().replace("btnCtrlTable","") or 9999))
        self.status_table_buttons = sorted([b for b in all_btns if b.objectName().startswith("btnStatusTable")],      key=lambda b:int(b.objectName().replace("btnStatusTable","") or 9999))


        # 로봇 버튼 그룹 설정
        self.btnRobot1.setCheckable(True)
        self.btnRobot2.setCheckable(True)
        self.robot_group = QButtonGroup(self)
        self.robot_group.setExclusive(False)  # 독점 모드 해제 (둘 다 눌릴 수도 있음)
        self.robot_group.addButton(self.btnRobot1)
        self.robot_group.addButton(self.btnRobot2)

        # 토글/연결
        self.btnRobot1.clicked.connect(lambda: self._toggle_robot(self.btnRobot1))
        self.btnRobot2.clicked.connect(lambda: self._toggle_robot(self.btnRobot2))
        self.ctrl_group=QButtonGroup(self); self.ctrl_group.setExclusive(True)
        for b in self.ctrl_table_buttons: self.ctrl_group.addButton(b); b.clicked.connect(lambda _,bt=b:self._on_click_ctrl_table(bt))
        self.status_group=QButtonGroup(self); self.status_group.setExclusive(True)
        for b in self.status_table_buttons: b.setCheckable(True); self.status_group.addButton(b); b.clicked.connect(lambda _,bt=b:self._on_click_status_table(bt))

        self.btnCallRobot.clicked.connect(self._on_click_call_robot)
        self.btnGoCharge.clicked.connect(self._on_click_go_charge)
        self.btnEStop.clicked.connect(self._on_click_estop)
        self.btnPayment.clicked.connect(self._on_click_payment)
        self.btnSales.clicked.connect(self._on_click_sales)

        # 스타일
        self.BTN_STYLE={"default":"","moving":"background-color:#3b82f6; color:white;","prev":"background-color:#f59e0b; color:black;","stopped":"background-color:#ef4444; color:white;","arrived":"background-color:#10b981; color:white;","estop":"background-color:#ef4444; color:white;"}
        self._orig_style={b:(b.styleSheet() or "") for b in [self.btnRobot1,self.btnRobot2,self.btnCallRobot,self.btnGoCharge,self.btnEStop,self.btnPayment,self.btnSales,*self.ctrl_table_buttons,*self.status_table_buttons]}

        # 상태/데이터
        self._current_dest_button=None; self._prev_button=None; self._estop_active=False
        self._orders:dict[int,list]=defaultdict(list); self._waiter_call_flag=dict()

        self._ensure_db(); self.setWindowTitle("POS Control")

    # -------- ROS -> GUI --------
    @QtCore.pyqtSlot(str, str)
    def on_nav_status(self, status: str, location_key: str):
        btn=self._button_from_location_key(location_key)
        if not btn: return
        if status=="moving": self._mark_moving(btn)
        elif status=="arrived": self._mark_arrived(btn)
        else: self._mark_stopped(btn)

    @QtCore.pyqtSlot(int, str, str)
    def on_order_request_popup(self, table_id: int, client_order_id: str, items_json: str):
        data = _jloads(items_json)
        # dict 또는 [dict, dict, ...] 모두 처리
        if isinstance(data, list):
            pretty_text = _items_to_text(_merge_item_dicts(data))
        elif isinstance(data, dict):
            pretty_text = _items_to_text(data)
        else:
            pretty_text = "(주문 내역 없음)"
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("주문 확인")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText(f"[테이블 {table_id}] 주문이 도착했습니다.\n\n{pretty_text}\n\n수락하시겠습니까?")
        a=msg.addButton("수락", QtWidgets.QMessageBox.AcceptRole); r=msg.addButton("거절", QtWidgets.QMessageBox.RejectRole)
        msg.exec_(); accepted=(msg.clickedButton()==a)
        if accepted:
            self._orders[int(table_id)].append(_jloads(items_json) or {})
            cur=self._current_status_selected_button()
            if cur and self._table_number_from_button(cur,"btnStatusTable")==int(table_id): self._show_table_orders(table_id)
        self.orderDecision.emit(client_order_id, bool(accepted))

    @QtCore.pyqtSlot(int)
    def on_waiter_call(self, table_no: int):
        btn=self._status_btn_by_num(int(table_no))
        if btn: self._set_style(btn,"stopped"); self._waiter_call_flag[btn]=True

    @QtCore.pyqtSlot(bool)
    def on_confirm_receipt(self, ok: bool):
        if ok: self.btnCallRobot.click()

    # -------- 버튼 핸들러 --------
    def _require_robot_selected(self)->bool:
        if not (self.btnRobot1.isChecked() or self.btnRobot2.isChecked()):
            QMessageBox.information(self,"안내","로봇(서빙로봇1/2) 중 하나를 선택하세요.")
            return False
        return True
    def _toggle_robot(self, btn):
        if btn.isChecked():
            other = self.btnRobot2 if btn is self.btnRobot1 else self.btnRobot1
            other.setChecked(False)
        else:
            btn.setChecked(False)

    def _on_click_call_robot(self):
        if not self._require_robot_selected(): return
        self._clear_estop_style()
        x,y,yaw=self.nav_points["call"]; self.requestNavGoal.emit("CALL",float(x),float(y),float(yaw))
        self._mark_moving(self.btnCallRobot)

    def _on_click_go_charge(self):
        if not self._require_robot_selected(): return
        self._clear_estop_style()
        x,y,yaw=self.nav_points["charge"]; self.requestNavGoal.emit("CHARGE",float(x),float(y),float(yaw))
        self._mark_moving(self.btnGoCharge)

    def _on_click_ctrl_table(self, btn):
        if not self._require_robot_selected(): return
        self._clear_estop_style()
        n=self._table_number_from_button(btn,"btnCtrlTable")
        pose=self.nav_points["tables"].get(n)
        if not pose: QMessageBox.warning(self,"오류",f"테이블 {n} 좌표가 없습니다."); return
        x,y,yaw=pose; self.requestNavGoal.emit(f"TABLE-{n}",float(x),float(y),float(yaw)); self._mark_moving(btn)

    def _on_click_status_table(self, btn):
        if self._waiter_call_flag.get(btn): self._waiter_call_flag[btn]=False; self._restore_default(btn)
        n=self._table_number_from_button(btn,"btnStatusTable")
        if n is not None: self._show_table_orders(n)

    def _on_click_estop(self):
        if not self._require_robot_selected(): return
        self.requestCancel.emit(); self.requestZeroTwist.emit(0.8)
        self._estop_active=True; self._set_style(self.btnEStop,"estop")
        if self._current_dest_button: self._mark_stopped(self._current_dest_button)

    def _on_click_payment(self):
        btn=self._current_status_selected_button()
        if not btn: QMessageBox.information(self,"안내","결제할 테이블을 우측 상태 버튼에서 선택하세요."); return
        n=self._table_number_from_button(btn,"btnStatusTable"); items=self._orders.get(int(n),[])
        if n is None: QMessageBox.warning(self,"오류","테이블 번호 추출 실패."); return
        if not items: QMessageBox.information(self,"안내",f"테이블 {n} 주문내역이 비어 있습니다."); return
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("INSERT INTO orders(table_id,items_json,created_at) VALUES(?,?,?)",
                             (str(n), json.dumps(items,ensure_ascii=False), datetime.now().isoformat()))
            self._orders[int(n)].clear(); self.txtOrderLog.clear()
            QMessageBox.information(self,"완료",f"테이블 {n} 결제 완료 및 초기화되었습니다.")
        except Exception as e:
            QMessageBox.critical(self,"DB 오류",f"주문 저장 실패: {e}")

    def _on_click_sales(self):
        dlg = QDialog(self); dlg.setWindowTitle("매출 내역")
        layout = QVBoxLayout(dlg); txt = QTextEdit(dlg); txt.setReadOnly(True)

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT id, table_id, items_json, created_at FROM orders ORDER BY id DESC")
            rows = cur.fetchall()
            conn.close()

            if not rows:
                txt.setPlainText("저장된 매출 내역이 없습니다.")
            else:
                lines = []
                for rid, tid, items_json, ts in rows:
                    data = _jloads(items_json)
                    if isinstance(data, list): body = _items_to_text(_merge_item_dicts(data))
                    elif isinstance(data, dict): body = _items_to_text(data)
                    else: body = "(주문 내역 없음)"
                    lines.append(f"[{rid}] 테이블 {tid} | {ts}\n{body}\n")
                txt.setPlainText("\n".join(lines))
        except Exception as e:
            txt.setPlainText(f"조회 실패: {e}")

        layout.addWidget(txt)
        btn_close = QPushButton("닫기", dlg); btn_close.clicked.connect(dlg.accept)
        layout.addWidget(btn_close); dlg.resize(600, 500); dlg.exec_()

    def _show_table_orders(self, table_no: int):
        items = self._orders.get(int(table_no), [])
        if not items:
            self.txtOrderLog.setPlainText("(주문 내역 없음)")
            return
        merged = _merge_item_dicts(items)
        self.txtOrderLog.setPlainText(_items_to_text(merged))


    # -------- 보조/스타일 --------
    def _set_style(self, btn, key): btn.setStyleSheet(self.BTN_STYLE.get(key,""))
    def _restore_default(self, btn): btn.setStyleSheet(self._orig_style.get(btn,""))
    def _mark_moving(self, btn):
        if self._current_dest_button and self._current_dest_button is not btn:
            self._set_style(self._current_dest_button,"prev"); self._prev_button=self._current_dest_button
        self._set_style(btn,"moving"); self._current_dest_button=btn
    def _mark_arrived(self, btn):
        self._set_style(btn,"arrived")
        if self._prev_button: self._restore_default(self._prev_button); self._prev_button=None
        self._current_dest_button=btn
    def _mark_stopped(self, btn): self._set_style(btn,"stopped")
    def _clear_estop_style(self):
        if self._estop_active: self._estop_active=False; self._restore_default(self.btnEStop)

    def _current_status_selected_button(self):
        for b in self.status_table_buttons:
            if b.isChecked(): return b
    def _table_number_from_button(self, btn, prefix):
        if not btn: return None
        s=btn.objectName().replace(prefix,"")
        return int(s) if s.isdigit() else None
    def _button_from_location_key(self, key: str):
        if key=="CALL": return self.btnCallRobot
        if key=="CHARGE": return self.btnGoCharge
        if key.startswith("TABLE-"):
            try: n=int(key.split("-",1)[1])
            except Exception: return None
            for b in self.ctrl_table_buttons:
                if self._table_number_from_button(b,"btnCtrlTable")==n: return b
    def _status_btn_by_num(self, n:int):
        for b in self.status_table_buttons:
            if self._table_number_from_button(b,"btnStatusTable")==n: return b

    def _ensure_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""CREATE TABLE IF NOT EXISTS orders(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    table_id TEXT NOT NULL,
                    items_json TEXT NOT NULL,
                    created_at TEXT NOT NULL)""")
        except Exception as e:
            QMessageBox.critical(self,"DB 오류",f"DB 초기화 실패: {e}")
