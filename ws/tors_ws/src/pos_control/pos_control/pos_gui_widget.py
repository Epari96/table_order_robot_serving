#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, sqlite3
from datetime import datetime
from collections import defaultdict

from PyQt5 import QtWidgets, QtCore, QtGui, uic
from PyQt5.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QTextEdit, QPushButton, QButtonGroup

class PosGuiWidget(QtWidgets.QMainWindow):
    # GUI -> ROS
    requestNavGoal    = QtCore.pyqtSignal(str, float, float, float)
    requestCancel     = QtCore.pyqtSignal()
    requestZeroTwist  = QtCore.pyqtSignal(float)
    orderDecision     = QtCore.pyqtSignal(str, bool)

    def __init__(self, ui_path: str, nav_points: dict, db_path: str):
        super().__init__()
        self.ui_path, self.nav_points, self.db_path = ui_path, nav_points, db_path
        if not os.path.exists(self.ui_path):
            QtWidgets.QMessageBox.critical(self, "UI Error", f"UI file not found: {self.ui_path}")
            raise SystemExit(1)
        self.ui = uic.loadUi(self.ui_path, self)

        # --- 필수 단일 위젯 ---
        self.btnRobot1: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnRobot1")
        self.btnRobot2: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnRobot2")
        self.btnCallRobot: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnCallRobot")
        self.btnGoCharge: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnGoCharge")
        self.btnEStop: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnEStop")
        self.btnPayment: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnPayment")
        self.btnSales: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "btnSales")
        self.txtOrderLog: QtWidgets.QTextEdit = self.findChild(QtWidgets.QTextEdit, "txtOrderLog")

        # --- 테이블 버튼 수집 (A안: 권장 네이밍, + 호환) ---
        all_btns = self.findChildren(QtWidgets.QPushButton)
        def pick(prefix): return [b for b in all_btns if b.objectName().startswith(prefix)]
        ctrl_candidates   = pick("btnCtrlTable") or pick("btnTable")
        status_candidates = pick("btnTable")     # 상태 세트가 없으면 아래에서 공유 처리

        def _num(prefix, name):
            suf = name.replace(prefix, "")
            return int(suf) if suf.isdigit() else 9999
        def sort_btns(btns):
            if not btns: return []
            name0 = btns[0].objectName()
            prefix = "btnCtrlTable" if name0.startswith("btnCtrlTable") else "btnTable"
            return sorted(btns, key=lambda b: _num(prefix, b.objectName()))

        self.ctrl_table_buttons   = sort_btns(ctrl_candidates)
        self.status_table_buttons = sort_btns(status_candidates)

        # 필수 체크(관대하게): 단일 위젯 + 테이블 버튼 세트 최소 1개
        missing = [n for n,w in {
            "btnRobot1": self.btnRobot1, "btnRobot2": self.btnRobot2,
            "btnCallRobot": self.btnCallRobot, "btnGoCharge": self.btnGoCharge,
            "btnEStop": self.btnEStop, "btnPayment": self.btnPayment,
            "btnSales": self.btnSales, "txtOrderLog": self.txtOrderLog,
        }.items() if w is None]
        if len(self.ctrl_table_buttons) == 0:
            missing.append("btnCtrlTable1..N 또는 btnTable1..N (테이블 버튼 세트가 1개도 없음)")

        if len(self.ctrl_table_buttons) == 0:
            missing.append("btnCtrlTable1..N (좌측 컨트롤용)")
        if len(self.status_table_buttons) == 0:
            missing.append("btnTable1..N (우측 상태/주문용)")

        if missing:
            QtWidgets.QMessageBox.critical(
                self, "UI Error",
                "다음 objectName이 UI에 없습니다:\n  - " + "\n  - ".join(missing) +
                "\n\nPosControl.ui에서 좌=btnCtrlTableN, 우=btnTableN을 모두 배치하세요."
            )
            raise SystemExit(2)

        # --- 그룹/토글/연결 ---
        self.btnRobot1.setCheckable(True); self.btnRobot2.setCheckable(True)
        self.robot_group = QButtonGroup(self); self.robot_group.setExclusive(True)
        self.robot_group.addButton(self.btnRobot1); self.robot_group.addButton(self.btnRobot2)
        # 재클릭하면 해제
        self.btnRobot1.clicked.connect(lambda: self._toggle_robot(self.btnRobot1))
        self.btnRobot2.clicked.connect(lambda: self._toggle_robot(self.btnRobot2))

        self.ctrl_group = QButtonGroup(self); self.ctrl_group.setExclusive(True)
        for b in self.ctrl_table_buttons:
            b.setCheckable(True); self.ctrl_group.addButton(b)
            b.clicked.connect(lambda _, bt=b: self._on_click_ctrl_table(bt))

        self.status_group = QButtonGroup(self); self.status_group.setExclusive(True)
        for b in self.status_table_buttons:
            b.setCheckable(True); self.status_group.addButton(b)
            b.clicked.connect(lambda _, bt=b: self._on_click_status_table(bt))

        # 기타 버튼
        self.btnCallRobot.clicked.connect(self._on_click_call_robot)
        self.btnGoCharge.clicked.connect(self._on_click_go_charge)
        self.btnEStop.clicked.connect(self._on_click_estop)
        self.btnPayment.clicked.connect(self._on_click_payment)
        self.btnSales.clicked.connect(self._on_click_sales)

        # 스타일
        self.BTN_STYLE = {
            "default":"", "moving":"background-color:#3b82f6; color:white;",
            "prev":"background-color:#f59e0b; color:black;",
            "stopped":"background-color:#ef4444; color:white;",
            "arrived":"background-color:#10b981; color:white;", "estop":"background-color:#ef4444; color:white;"
        }
        self._orig_style = {}
        for b in [self.btnRobot1, self.btnRobot2, self.btnCallRobot, self.btnGoCharge, self.btnEStop,
                  *self.ctrl_table_buttons, *self.status_table_buttons, self.btnPayment, self.btnSales]:
            self._orig_style[b] = b.styleSheet() or ""

        # 상태
        self._current_dest_button = None
        self._prev_button = None
        self._estop_active = False
        self._orders: dict[int, list] = defaultdict(list)  # int table_id
        self._waiter_call_flag: dict[QtWidgets.QPushButton, bool] = defaultdict(bool)

        self._ensure_db()
        self.setWindowTitle("POS Control")

    # ===== ROS → GUI 슬롯 (int table_id) =====
    @QtCore.pyqtSlot(str, str)
    def on_nav_status(self, status: str, location_key: str):
        btn = self._button_from_location_key(location_key)
        if not btn: return
        if status == "moving": self._mark_moving(btn)
        elif status == "arrived": self._mark_arrived(btn)
        else: self._mark_stopped(btn)

    @QtCore.pyqtSlot(int, str, str)
    def on_order_request_popup(self, table_id: int, client_order_id: str, items_json: str):
        try: pretty = json.dumps(json.loads(items_json), ensure_ascii=False, indent=2)
        except Exception: pretty = items_json
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("주문 확인"); msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText(f"[테이블 {table_id}] 주문이 도착했습니다.\n\n{pretty}\n\n수락하시겠습니까?")
        accept_btn = msg.addButton("수락", QtWidgets.QMessageBox.AcceptRole)
        reject_btn = msg.addButton("거절", QtWidgets.QMessageBox.RejectRole)
        msg.exec_()
        accepted = (msg.clickedButton() == accept_btn)

        if accepted:
            try: self._orders[int(table_id)].append(json.loads(items_json) if items_json else {})
            except Exception: self._orders[int(table_id)].append(items_json)
            cur_btn = self._current_status_selected_button()
            cur_no  = self._table_number_from_button(cur_btn, "btnTable") if cur_btn else None
            if cur_no == int(table_id): self._show_table_orders(cur_no)

        self.orderDecision.emit(client_order_id, bool(accepted))

    @QtCore.pyqtSlot(int)
    def on_waiter_call(self, table_no: int):
        # 상태(오른쪽) 버튼을 빨강으로
        btn = None
        for b in self.status_table_buttons:
            if self._table_number_from_button(b, "btnTable") == int(table_no):
                btn = b; break
        if btn:
            self._set_style(btn, "stopped")
            self._waiter_call_flag[btn] = True

    @QtCore.pyqtSlot(bool)
    def on_confirm_receipt(self, ok: bool):
        if ok: self.btnCallRobot.click()

    # ===== 버튼 핸들러 =====
    def _require_robot_selected(self) -> bool:
        if not (self.btnRobot1.isChecked() or self.btnRobot2.isChecked()):
            QMessageBox.information(self, "안내", "로봇(서빙로봇1/2) 중 하나를 선택하세요.")
            return False
        return True

    def _toggle_robot(self, clicked_btn: QtWidgets.QPushButton):
        other = self.btnRobot2 if clicked_btn is self.btnRobot1 else self.btnRobot1
        if clicked_btn.isChecked() and not other.isChecked():
            clicked_btn.setChecked(False)

    def _on_click_call_robot(self):
        if not self._require_robot_selected(): return
        self._clear_estop_style()
        x,y,yaw = self.nav_points["call"]
        self.requestNavGoal.emit("CALL", float(x), float(y), float(yaw))
        self._mark_moving(self.btnCallRobot)

    def _on_click_go_charge(self):
        if not self._require_robot_selected(): return
        self._clear_estop_style()
        x,y,yaw = self.nav_points["charge"]
        self.requestNavGoal.emit("CHARGE", float(x), float(y), float(yaw))
        self._mark_moving(self.btnGoCharge)

    def _on_click_ctrl_table(self, btn: QtWidgets.QPushButton):
        if not self._require_robot_selected(): return
        self._clear_estop_style()
        table_no = self._table_number_from_button(btn, "btnCtrlTable")
        pose = self.nav_points["tables"].get(table_no)
        if not pose:
            QMessageBox.warning(self, "오류", f"테이블 {table_no} 좌표가 없습니다."); return
        x,y,yaw = pose
        self.requestNavGoal.emit(f"TABLE-{table_no}", float(x), float(y), float(yaw))
        self._mark_moving(btn)

    def _on_click_status_table(self, btn: QtWidgets.QPushButton):
        if self._waiter_call_flag.get(btn, False):
            self._waiter_call_flag[btn] = False; self._restore_default(btn)
        table_no = self._table_number_from_button(btn, "btnTable")
        if table_no is not None: self._show_table_orders(table_no)

    def _on_click_estop(self):
        self.requestCancel.emit(); self.requestZeroTwist.emit(0.8)
        self._estop_active = True; self._set_style(self.btnEStop, "estop")
        if self._current_dest_button: self._mark_stopped(self._current_dest_button)

    def _on_click_payment(self):
        table_btn = self._current_status_selected_button()
        if not table_btn:
            QMessageBox.information(self, "안내", "결제할 테이블(오른쪽 상태 버튼)을 선택하세요."); return
        table_no = self._table_number_from_button(table_btn, "btnTable")
        if table_no is None: QMessageBox.warning(self, "오류", "테이블 번호 추출 실패."); return

        items_list = self._orders.get(int(table_no), [])
        if not items_list:
            QMessageBox.information(self, "안내", f"테이블 {table_no} 주문내역이 비어 있습니다."); return

        try:
            conn = sqlite3.connect(self.db_path); cur = conn.cursor()
            cur.execute("""INSERT INTO orders(table_id, items_json, created_at) VALUES (?,?,?)""",
                        (str(table_no), json.dumps(items_list, ensure_ascii=False), datetime.now().isoformat()))
            conn.commit(); conn.close()
        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"주문 저장 실패: {e}"); return

        self._orders[int(table_no)].clear(); self.txtOrderLog.clear()
        QMessageBox.information(self, "완료", f"테이블 {table_no} 결제 완료 및 초기화되었습니다.")

    def _on_click_sales(self):
        dlg = QDialog(self); dlg.setWindowTitle("매출 내역"); layout = QVBoxLayout(dlg)
        txt = QTextEdit(dlg); txt.setReadOnly(True)
        try:
            conn = sqlite3.connect(self.db_path); cur = conn.cursor()
            cur.execute("SELECT id, table_id, items_json, created_at FROM orders ORDER BY id DESC")
            rows = cur.fetchall(); conn.close()
            if not rows: txt.setText("저장된 매출 내역이 없습니다.")
            else:
                lines=[]
                for rid, tid, items_json, ts in rows:
                    try: items = json.loads(items_json)
                    except Exception: items = items_json
                    lines.append(f"[{rid}] 테이블 {tid} | {ts}\n{items}\n")
                txt.setText("\n".join(lines))
        except Exception as e:
            txt.setText(f"조회 실패: {e}")
        layout.addWidget(txt); btn_close = QPushButton("닫기", dlg); btn_close.clicked.connect(dlg.accept)
        layout.addWidget(btn_close); dlg.resize(600, 500); dlg.exec_()

    # ===== 보조 =====
    def _set_style(self, btn, key): btn.setStyleSheet(self.BTN_STYLE.get(key, ""))
    def _restore_default(self, btn): btn.setStyleSheet(self._orig_style.get(btn, ""))

    def _mark_moving(self, dest_btn):
        if self._current_dest_button and self._current_dest_button is not dest_btn:
            self._set_style(self._current_dest_button, "prev"); self._prev_button = self._current_dest_button
        self._set_style(dest_btn, "moving"); self._current_dest_button = dest_btn

    def _mark_arrived(self, dest_btn):
        self._set_style(dest_btn, "arrived")
        if self._prev_button: self._restore_default(self._prev_button); self._prev_button = None
        self._current_dest_button = dest_btn

    def _mark_stopped(self, dest_btn): self._set_style(dest_btn, "stopped")

    def _clear_estop_style(self):
        if self._estop_active: self._estop_active = False; self._restore_default(self.btnEStop)

    def _current_status_selected_button(self):
        for b in self.status_table_buttons:
            if b.isChecked(): return b
        return None

    def _current_ctrl_selected_button(self):
        for b in self.ctrl_table_buttons:
            if b.isChecked(): return b
        return None

    def _table_number_from_button(self, btn, prefix):
        if not btn: return None
        name = btn.objectName()
        if name.startswith(prefix):
            suf = name.replace(prefix, "")
            return int(suf) if suf.isdigit() else None
        return None

    def _button_from_location_key(self, key: str):
        if key == "CALL": return self.btnCallRobot
        if key == "CHARGE": return self.btnGoCharge
        if key.startswith("TABLE-"):
            try: n = int(key.split("-",1)[1])
            except Exception: return None
            for b in self.ctrl_table_buttons:
                if self._table_number_from_button(b, "btnCtrlTable") == n:
                    return b
        return None

    def _ensure_db(self):
        try:
            conn = sqlite3.connect(self.db_path); cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id TEXT NOT NULL,
                items_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""); conn.commit(); conn.close()
        except Exception as e:
            QMessageBox.critical(self, "DB 오류", f"DB 초기화 실패: {e}")
