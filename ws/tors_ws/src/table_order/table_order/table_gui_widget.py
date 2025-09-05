#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, uuid, re, os
from PyQt5 import QtWidgets, uic
from ament_index_python.packages import get_package_share_directory
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QScrollArea, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont

class MenuItemWidget(QGroupBox):
    addClicked = pyqtSignal(str, int)  # (item_name, qty)
    def __init__(self, item_name: str, cost: int, image_path: str = "", parent=None):
        super().__init__(parent)
        self.setTitle(""); self.setObjectName("menuCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed); self.setFixedHeight(150)
        self.item_name, self.cost, self.temp_qty = item_name, cost, 0

        self.imageLabel = QLabel(alignment=Qt.AlignCenter)
        if image_path:
            pm = QPixmap(image_path)
            if not pm.isNull():
                self.imageLabel.setPixmap(pm.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.nameLabel = QLabel(item_name, alignment=Qt.AlignCenter); self.nameLabel.setFont(QFont("", 11, QFont.Bold))

        left = QVBoxLayout(); left.addWidget(self.imageLabel); left.addWidget(self.nameLabel)

        self.costLabel = QLabel(f"가격: {cost}"); self.costLabel.setFont(QFont("", 10))
        self.qtyLabel  = QLabel("수량: 0"); self.qtyLabel.setFont(QFont("", 10))
        self.sumLabel  = QLabel("금액: 0"); self.sumLabel.setFont(QFont("", 10))
        self.btnPlus   = QPushButton("+"); self.btnPlus.setMinimumSize(10, 30)
        self.btnMinus  = QPushButton("-"); self.btnMinus.setMinimumSize(10, 30)
        self.btnAdd    = QPushButton("담기"); self.btnAdd.setMinimumSize(160, 30)

        qty_row = QHBoxLayout(); qty_row.addWidget(self.qtyLabel); qty_row.addSpacing(62); qty_row.addWidget(self.btnPlus); qty_row.addWidget(self.btnMinus)
        sum_row = QHBoxLayout(); sum_row.addWidget(self.sumLabel); sum_row.addWidget(self.btnAdd)

        right = QVBoxLayout(); right.addWidget(self.costLabel); right.addLayout(qty_row); right.addLayout(sum_row)
        root = QHBoxLayout(); root.addLayout(left); root.addLayout(right); self.setLayout(root)

        self.btnPlus.clicked.connect(self._inc); self.btnMinus.clicked.connect(self._dec); self.btnAdd.clicked.connect(self._emit_add)
        self.setStyleSheet("""QGroupBox#menuCard { border:1px solid #C8CCD0; border-radius:8px; padding:8px; background:#FAFAFA;}""")

    def _inc(self): self.temp_qty += 1; self._refresh_labels()
    def _dec(self): 
        if self.temp_qty > 0: self.temp_qty -= 1; self._refresh_labels()
    def _refresh_labels(self):
        self.qtyLabel.setText(f"수량: {self.temp_qty}"); self.sumLabel.setText(f"금액: {self.temp_qty * self.cost}")
    def _emit_add(self):
        if self.temp_qty > 0:
            self.addClicked.emit(self.item_name, self.temp_qty)
            self.temp_qty = 0; self._refresh_labels()

class TableOrderWindow(QtWidgets.QMainWindow):
    waiterClicked = pyqtSignal(int)                 # ← 테이블번호
    confirmReceiptClicked = pyqtSignal()
    orderClicked = pyqtSignal()
    orderPayload = pyqtSignal(int, str, object)     # ← (table_id:int, client_order_id, items_dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        share_dir = get_package_share_directory('table_order')
        ui_path = os.path.join(share_dir, 'resource', 'TableOrder.ui')
        uic.loadUi(ui_path, self)

        # 테이블 번호(라벨 텍스트와 동기)
        self.table_num = 2
        self.table_label = self.findChild(QLabel, "tableLabel")
        if self.table_label: self.table_label.setText(f"테이블 {self.table_num}")

        self.items = ["짜장면", "짬뽕", "탕수육", "제로 콜라"]
        self.cost  = {'짜장면':8000,'짬뽕':8500,'탕수육':20000,'제로 콜라':3000}
        image_dir = os.path.join(share_dir, 'resource')
        self.image_path = {i: os.path.join(image_dir, f"{i}.jpg") for i in self.items}

        self.order_data = {i:0 for i in self.items}
        self.order_history = {i:0 for i in self.items}
        self.order_history_total = 0

        self.menu_container  = self.findChild(QVBoxLayout, "menuContainerLayout")
        self.order_container = self.findChild(QVBoxLayout, "orderContainerLayout")
        self.total_label     = self.findChild(QLabel, "totalCostLabel")
        self.menu_scroll     = self.findChild(QScrollArea, "menuScrollArea")
        self.order_scroll    = self.findChild(QScrollArea, "orderScrollArea")

        for sa in (self.menu_scroll, self.order_scroll):
            if sa: sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        if self.menu_container: self.menu_container.setAlignment(Qt.AlignTop)
        if self.order_container: self.order_container.setAlignment(Qt.AlignTop)
        self.setMinimumSize(800, 420)

        for name in self.items:
            card = MenuItemWidget(name, self.cost[name], self.image_path[name])
            card.addClicked.connect(self.on_add_clicked)
            self._insert_top(self.menu_container, card)

        self.btn_history = self.findChild(QtWidgets.QPushButton, "historyButton")
        self.btn_waiter  = self.findChild(QtWidgets.QPushButton, "waiterButton")
        self.btn_confirm = self.findChild(QtWidgets.QPushButton, "confirmReceiptButton")
        self.btn_order   = self.findChild(QtWidgets.QPushButton, "orderButton")

        if self.btn_history: self.btn_history.clicked.connect(self.show_order_history)
        if self.btn_waiter:  self.btn_waiter.clicked.connect(lambda: self.waiterClicked.emit(self.table_num))
        if self.btn_confirm: self.btn_confirm.clicked.connect(self.confirmReceiptClicked.emit)
        if self.btn_order:   self.btn_order.clicked.connect(self.finalize_order)

        self.update_total_cost()
        self.setStyleSheet("""QGroupBox#orderCard { border:1px solid #D5D9DD; border-radius:8px; padding:6px; background:#FAFAFA;}""")

    def _insert_top(self, vlayout: QVBoxLayout, widget: QWidget):
        if not vlayout: return
        insert_index = max(0, vlayout.count() - 1)
        vlayout.insertWidget(insert_index, widget, 0, Qt.AlignTop)

    def _clear_order_cards(self):
        if not self.order_container: return
        for i in range(self.order_container.count()-1, -1, -1):
            it = self.order_container.itemAt(i)
            if not it or it.spacerItem() is not None: continue
            w = it.widget()
            if w:
                self.order_container.takeAt(i); w.deleteLater()

    def _make_order_card(self, item, quantity):
        box = QGroupBox(); box.setObjectName("orderCard"); box.setProperty("item_name", item)
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed); box.setFixedHeight(90)
        layout = QHBoxLayout()
        name_label = QLabel(item); name_label.setFont(QFont("", 12, QFont.Bold))
        qty_label  = QLabel(f"수량: {quantity}"); qty_label.setFont(QFont("", 10))
        btn_plus, btn_minus, btn_del = QPushButton("+"), QPushButton("-"), QPushButton("삭제")
        for b in (btn_plus, btn_minus, btn_del): b.setMinimumSize(30, 30)
        btn_plus.clicked.connect(lambda: self._adjust_order_qty(item, +1, qty_label, box))
        btn_minus.clicked.connect(lambda: self._adjust_order_qty(item, -1, qty_label, box))
        btn_del.clicked.connect(lambda: self._delete_order_card(box, item))
        for w in (name_label, qty_label, btn_plus, btn_minus, btn_del): layout.addWidget(w)
        box.setLayout(layout); return box

    def on_add_clicked(self, item, qty):
        self.order_data[item] += qty
        self._remove_order_card(item)
        self._insert_top(self.order_container, self._make_order_card(item, self.order_data[item]))
        self.update_total_cost()

    def _remove_order_card(self, item):
        if not self.order_container: return
        for i in range(self.order_container.count()-1, -1, -1):
            it = self.order_container.itemAt(i)
            if not it or it.spacerItem() is not None: continue
            w = it.widget()
            if w and w.property("item_name") == item:
                self.order_container.takeAt(i); w.deleteLater(); break

    def _delete_order_card(self, groupbox, item):
        self.order_data[item] = 0; self.order_container.removeWidget(groupbox)
        groupbox.deleteLater(); self.update_total_cost()

    def _adjust_order_qty(self, item, delta, qty_label, groupbox):
        self.order_data[item] = max(0, self.order_data[item] + delta)
        if self.order_data[item] == 0: self._delete_order_card(groupbox, item)
        else: qty_label.setText(f"수량: {self.order_data[item]}")
        self.update_total_cost()

    def finalize_order(self):
        client_order_id = str(uuid.uuid4())
        items_dict = self.get_order_summary()  # {이름: 수량}
        self.orderPayload.emit(int(self.table_num), client_order_id, items_dict)
        self.orderClicked.emit()
        for k, v in self.order_data.items():
            if v > 0:
                self.order_history[k] += v; self.order_history_total += v * self.cost[k]
        self._clear_order_cards(); self.order_data = {i:0 for i in self.items}
        self.update_total_cost()

    def update_total_cost(self):
        total = sum(self.order_data[i] * self.cost[i] for i in self.items)
        self.total_label.setText(f"총 금액: {total} 원  "); self.total_label.setFont(QFont("", 12, QFont.Bold))

    def show_order_history(self):
        lines = [f"{k}: {self.order_history.get(k,0)}개 (₩{self.order_history.get(k,0)*self.cost[k]:,})"
                 for k in self.items if self.order_history.get(k,0) > 0]
        text = "주문 내역이 없습니다." if not lines else "\n".join(lines)+f"\n\n총 합계: ₩{self.order_history_total:,}"
        QMessageBox.information(self, "주문내역", text)

    def get_order_summary(self) -> dict:
        return {k:v for k,v in getattr(self, "order_data", {}).items() if v > 0}
