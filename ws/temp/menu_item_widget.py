# widget.py
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGroupBox, QScrollArea, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont

# ------------------------------
# 왼쪽 메뉴 블록
# ------------------------------
class MenuItemWidget(QGroupBox):
    addClicked = pyqtSignal(str, int)  # (item_name, qty)

    def __init__(self, item_name: str, cost: int, image_path: str = "", parent=None):
        super().__init__(parent)
        self.setTitle("")
        self.setObjectName("menuCard")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(150)

        self.item_name = item_name
        self.cost = cost
        self.temp_qty = 0

        # Left: image + name
        self.imageLabel = QLabel(alignment=Qt.AlignCenter)
        if image_path:
            pm = QPixmap(image_path)
            if not pm.isNull():
                self.imageLabel.setPixmap(pm.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.nameLabel = QLabel(item_name, alignment=Qt.AlignCenter)
        self.nameLabel.setFont(QFont("", 11, QFont.Bold))

        left = QVBoxLayout()
        left.addWidget(self.imageLabel)
        left.addWidget(self.nameLabel)

        # Right: cost, qty row, sum/add row
        self.costLabel = QLabel(f"Cost: {cost}")
        self.qtyLabel  = QLabel("Quantity: 0")
        self.sumLabel  = QLabel("Sum Cost: 0")
        self.btnPlus   = QPushButton("+")
        self.btnPlus.setMinimumSize(10, 30)
        self.btnMinus  = QPushButton("-")
        self.btnMinus.setMinimumSize(10, 30)
        self.btnAdd    = QPushButton("담기")

        qty_row = QHBoxLayout()
        qty_row.addWidget(self.qtyLabel)
        qty_row.addSpacing(62)
        qty_row.addWidget(self.btnPlus)
        qty_row.addWidget(self.btnMinus)

        sum_row = QHBoxLayout()
        sum_row.addWidget(self.sumLabel)
        sum_row.addWidget(self.btnAdd)

        right = QVBoxLayout()
        right.addWidget(self.costLabel)
        right.addLayout(qty_row)
        right.addLayout(sum_row)

        root = QHBoxLayout()
        root.addLayout(left)
        root.addLayout(right)
        self.setLayout(root)

        # Signals
        self.btnPlus.clicked.connect(self._inc)
        self.btnMinus.clicked.connect(self._dec)
        self.btnAdd.clicked.connect(self._emit_add)

        # 스타일(블록)
        self.setStyleSheet("""
            QGroupBox#menuCard {
                border: 1px solid #C8CCD0;
                border-radius: 8px;
                padding: 8px;
                background: #FAFAFA;
            }
        """)

    def _inc(self):
        self.temp_qty += 1
        self._refresh_labels()

    def _dec(self):
        if self.temp_qty > 0:
            self.temp_qty -= 1
            self._refresh_labels()

    def _refresh_labels(self):
        self.qtyLabel.setText(f"Quantity: {self.temp_qty}")
        self.sumLabel.setText(f"Sum Cost: {self.temp_qty * self.cost}")

    def _emit_add(self):
        if self.temp_qty > 0:
            self.addClicked.emit(self.item_name, self.temp_qty)
            self.temp_qty = 0
            self._refresh_labels()


# ------------------------------
# 메인 윈도우
# ------------------------------
class TableOrderWindow(QtWidgets.QMainWindow):
    waiterClicked = pyqtSignal()
    confirmReceiptClicked = pyqtSignal()
    orderClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("MainWindow.ui", self)

        # 테이블 번호 라벨을 코드에서 수정
        self.table_label = self.findChild(QLabel, "tableLabel")
        if self.table_label:
            self.table_label.setText(f"테이블 14")

        # 데이터
        self.items = ["짜장면", "짬뽕", "탕수육", "제로 콜라"]
        self.cost  = {'짜장면': 8000, '짬뽕': 8500, '탕수육': 20000, '제로 콜라': 3000}
        self.image_path = {i: f"{i}.jpg" for i in self.items}

        # 상태
        self.order_data = {i: 0 for i in self.items}   # 현재 장바구니
        self.order_history = {i: 0 for i in self.items}  # 누적 주문 내역
        self.order_history_total = 0

        # .ui 핸들
        self.menu_container  = self.findChild(QVBoxLayout, "menuContainerLayout")
        self.order_container = self.findChild(QVBoxLayout, "orderContainerLayout")
        self.total_label     = self.findChild(QLabel,       "totalCostLabel")
        self.menu_scroll     = self.findChild(QScrollArea, "menuScrollArea")
        self.order_scroll    = self.findChild(QScrollArea, "orderScrollArea")

        # 스크롤/정렬/최소크기
        for sa in (self.menu_scroll, self.order_scroll):
            if sa:
                sa.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        if self.menu_container:
            self.menu_container.setAlignment(Qt.AlignTop)
        if self.order_container:
            self.order_container.setAlignment(Qt.AlignTop)
        self.setMinimumSize(800, 420)

        # 왼쪽 메뉴 카드 생성
        for name in self.items:
            card = MenuItemWidget(name, self.cost[name], self.image_path[name])
            card.addClicked.connect(self.on_add_clicked)
            self._insert_top(self.menu_container, card)

        # 버튼들
        self.btn_history = self.findChild(QtWidgets.QPushButton, "historyButton")
        self.btn_waiter  = self.findChild(QtWidgets.QPushButton, "waiterButton")
        self.btn_confirm = self.findChild(QtWidgets.QPushButton, "confirmReceiptButton")
        self.btn_order   = self.findChild(QtWidgets.QPushButton, "orderButton")

        if self.btn_history:
            self.btn_history.clicked.connect(self.show_order_history)
        if self.btn_waiter:
            self.btn_waiter.clicked.connect(self.waiterClicked.emit)
        if self.btn_confirm:
            self.btn_confirm.clicked.connect(self.confirmReceiptClicked.emit)
        if self.btn_order:
            self.btn_order.clicked.connect(self.finalize_order)

        self.update_total_cost()

        # 오른쪽 카드 공통 스타일
        self.setStyleSheet("""
            QGroupBox#orderCard {
                border: 1px solid #D5D9DD;
                border-radius: 8px;
                padding: 6px;
                background: #FAFAFA;
            }
        """)

    # 유틸
    def _insert_top(self, vlayout: QVBoxLayout, widget: QWidget):
        if vlayout is None:
            return
        insert_index = max(0, vlayout.count() - 1)  # 마지막은 spacer
        vlayout.insertWidget(insert_index, widget, 0, Qt.AlignTop)

    def _clear_order_cards(self):
        if self.order_container is None:
            return
        for i in range(self.order_container.count() - 1, -1, -1):
            item = self.order_container.itemAt(i)
            if not item or item.spacerItem() is not None:
                continue
            w = item.widget()
            if w:
                self.order_container.takeAt(i)
                w.deleteLater()

    def _make_order_card(self, item, quantity):
        box = QGroupBox()
        box.setObjectName("orderCard")
        box.setProperty("item_name", item)
        box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        box.setFixedHeight(90)

        layout = QHBoxLayout()
        name_label = QLabel(item)
        qty_label  = QLabel(f"Quantity: {quantity}")
        btn_plus   = QPushButton("+")
        btn_plus.setMinimumSize(30, 30)
        btn_minus  = QPushButton("-")
        btn_minus.setMinimumSize(30, 30)
        btn_del    = QPushButton("삭제")
        btn_del.setMinimumSize(50, 30)

        btn_plus.clicked.connect(lambda: self._adjust_order_qty(item, +1, qty_label, box))
        btn_minus.clicked.connect(lambda: self._adjust_order_qty(item, -1, qty_label, box))
        btn_del.clicked.connect(lambda: self._delete_order_card(box, item))

        for w in (name_label, qty_label, btn_plus, btn_minus, btn_del):
            layout.addWidget(w)
        box.setLayout(layout)
        return box

    # 동작
    def on_add_clicked(self, item, qty):
        self.order_data[item] += qty
        self._remove_order_card(item)
        self._insert_top(self.order_container, self._make_order_card(item, self.order_data[item]))
        self.update_total_cost()

    def _remove_order_card(self, item):
        if self.order_container is None:
            return
        for i in range(self.order_container.count() - 1, -1, -1):
            it = self.order_container.itemAt(i)
            if not it or it.spacerItem() is not None:
                continue
            w = it.widget()
            if w and w.property("item_name") == item:
                self.order_container.takeAt(i)
                w.deleteLater()
                break

    def _delete_order_card(self, groupbox, item):
        self.order_data[item] = 0
        self.order_container.removeWidget(groupbox)
        groupbox.deleteLater()
        self.update_total_cost()

    def _adjust_order_qty(self, item, delta, qty_label, groupbox):
        self.order_data[item] = max(0, self.order_data[item] + delta)
        if self.order_data[item] == 0:
            self._delete_order_card(groupbox, item)
        else:
            qty_label.setText(f"Quantity: {self.order_data[item]}")
        self.update_total_cost()

    def finalize_order(self):
        self.orderClicked.emit()  # 외부 알림(선택)
        for k, v in self.order_data.items():
            if v > 0:
                self.order_history[k] += v
                self.order_history_total += v * self.cost[k]
        self._clear_order_cards()
        self.order_data = {i: 0 for i in self.items}
        self.update_total_cost()

    def update_total_cost(self):
        total = sum(self.order_data[i] * self.cost[i] for i in self.items)
        self.total_label.setText(f"Total Cost: {total}")

    def show_order_history(self):
        lines = []
        for k in self.items:
            q = self.order_history.get(k, 0)
            if q > 0:
                lines.append(f"{k}: {q}개 (₩{q*self.cost[k]:,})")
        if not lines:
            text = "주문 내역이 없습니다."
        else:
            text = "\n".join(lines) + f"\n\n총 합계: ₩{self.order_history_total:,}"
        QMessageBox.information(self, "주문내역", text)
