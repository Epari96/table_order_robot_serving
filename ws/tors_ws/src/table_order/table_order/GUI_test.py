# table_order_demo.py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QGroupBox, QHBoxLayout

class TableOrderDemo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("../resource/table_order.ui", self)  # 같은 폴더의 .ui 로드

        # 데이터 모델
        self.items = ["짜장면", "짬뽕", "탕수육", "제로 콜라"]
        self.cost = {'짜장면': 8000, '짬뽕': 8500, '탕수육': 20000, '제로 콜라': 3000}
        self.temp_order_data = {i: 0 for i in self.items}   # 왼쪽 임시 수량
        self.order_data = {i: 0 for i in self.items}        # 오른쪽 장바구니 수량

        # .ui의 위젯 이름과 아이템 키를 연결하기 위한 매핑
        self.btn_plus = {
            "짜장면": self.findChild(QPushButton, "plusButton_jjajang"),
            "짬뽕": self.findChild(QPushButton, "plusButton_jjamppong"),
            "탕수육": self.findChild(QPushButton, "plusButton_tangsuyuk"),
            "제로 콜라": self.findChild(QPushButton, "plusButton_zeroCola"),
        }
        self.btn_minus = {
            "짜장면": self.findChild(QPushButton, "minusButton_jjajang"),
            "짬뽕": self.findChild(QPushButton, "minusButton_jjamppong"),
            "탕수육": self.findChild(QPushButton, "minusButton_tangsuyuk"),
            "제로 콜라": self.findChild(QPushButton, "minusButton_zeroCola"),
        }
        self.btn_add = {
            "짜장면": self.findChild(QPushButton, "addButton_jjajang"),
            "짬뽕": self.findChild(QPushButton, "addButton_jjamppong"),
            "탕수육": self.findChild(QPushButton, "addButton_tangsuyuk"),
            "제로 콜라": self.findChild(QPushButton, "addButton_zeroCola"),
        }
        self.lbl_qty = {
            "짜장면": self.findChild(QLabel, "quantityLabel_jjajang"),
            "짬뽕": self.findChild(QLabel, "quantityLabel_jjamppong"),
            "탕수육": self.findChild(QLabel, "quantityLabel_tangsuyuk"),
            "제로 콜라": self.findChild(QLabel, "quantityLabel_zeroCola"),
        }
        self.lbl_sum = {
            "짜장면": self.findChild(QLabel, "sumCostLabel_jjajang"),
            "짬뽕": self.findChild(QLabel, "sumCostLabel_jjamppong"),
            "탕수육": self.findChild(QLabel, "sumCostLabel_tangsuyuk"),
            "제로 콜라": self.findChild(QLabel, "sumCostLabel_zeroCola"),
        }
        self.lbl_total = self.findChild(QLabel, "totalCostLabel")
        self.scroll_layout = self.findChild(type(self).findChild(self.__class__, "verticalLayout_scroll".__class__), "verticalLayout_scroll")
        # 위 한 줄은 타입 추론 회피용 꼼수라 가독성이 떨어집니다. 아래처럼 다시 안전하게 찾습니다.
        from PyQt5.QtWidgets import QVBoxLayout
        self.scroll_layout = self.findChild(QVBoxLayout, "verticalLayout_scroll")

        # 시그널 연결
        for item in self.items:
            self.btn_plus[item].clicked.connect(lambda _, it=item: self.adjust_temp_quantity(it, +1))
            self.btn_minus[item].clicked.connect(lambda _, it=item: self.adjust_temp_quantity(it, -1))
            self.btn_add[item].clicked.connect(lambda _, it=item: self.add_to_right_list(it))

        # 옵션: 주문 버튼은 현재 담긴 품목/수량을 콘솔로 출력만
        order_btn = self.findChild(QPushButton, "orderButton")
        if order_btn:
            order_btn.clicked.connect(self.print_order)

        self.update_total_cost()

    # ----- 왼쪽 수량/소계 갱신 -----
    def adjust_temp_quantity(self, item, delta):
        self.temp_order_data[item] = max(0, self.temp_order_data[item] + delta)
        qty = self.temp_order_data[item]
        self.lbl_qty[item].setText(f"Quantity: {qty}")
        self.lbl_sum[item].setText(f"Sum Cost: {qty * self.cost[item]}")

    # ----- 오른쪽 카드(그룹박스) 추가/업데이트 -----
    def add_to_right_list(self, item):
        # 주문 수량 반영
        if self.temp_order_data[item] == 0:
            return
        self.order_data[item] += self.temp_order_data[item]
        self.temp_order_data[item] = 0
        self.lbl_qty[item].setText("Quantity: 0")
        self.lbl_sum[item].setText("Sum Cost: 0")

        # 기존 카드 있으면 제거 후 재생성(수량 업데이트)
        self.remove_card_if_exists(item)
        self.create_item_card(item, self.order_data[item])
        self.update_total_cost()

    def remove_card_if_exists(self, item):
        # scroll_layout 안의 위젯들을 뒤에서부터 검사
        for i in range(self.scroll_layout.count() - 1, -1, -1):
            w = self.scroll_layout.itemAt(i).widget()
            if w and w.property("item_name") == item:
                self.scroll_layout.takeAt(i)
                w.deleteLater()

    def create_item_card(self, item, quantity):
        groupbox = QGroupBox()
        groupbox.setProperty("item_name", item)
        groupbox.setFixedHeight(100)
        layout = QHBoxLayout()

        name_label = QLabel(item)
        qty_label = QLabel(f"Quantity: {quantity}")
        btn_plus = QPushButton("+")
        btn_minus = QPushButton("-")
        btn_delete = QPushButton("삭제")

        btn_plus.clicked.connect(lambda: self.adjust_right_quantity(item, +1, qty_label, groupbox))
        btn_minus.clicked.connect(lambda: self.adjust_right_quantity(item, -1, qty_label, groupbox))
        btn_delete.clicked.connect(lambda: self.delete_item_card(groupbox, item))

        for w in (name_label, qty_label, btn_plus, btn_minus, btn_delete):
            layout.addWidget(w)

        groupbox.setLayout(layout)
        self.scroll_layout.addWidget(groupbox)

    def delete_item_card(self, groupbox, item):
        self.order_data[item] = 0
        self.scroll_layout.removeWidget(groupbox)
        groupbox.deleteLater()
        self.update_total_cost()

    def adjust_right_quantity(self, item, delta, qty_label, groupbox):
        self.order_data[item] = max(0, self.order_data[item] + delta)
        if self.order_data[item] == 0:
            # 0이면 카드 삭제
            self.delete_item_card(groupbox, item)
        else:
            qty_label.setText(f"Quantity: {self.order_data[item]}")
        self.update_total_cost()

    # ----- 총액 -----
    def update_total_cost(self):
        total = sum(self.order_data[i] * self.cost[i] for i in self.items)
        self.lbl_total.setText(f"Total Cost: {total}")

    # ----- 데모용 출력 -----
    def print_order(self):
        print("=== ORDER ===")
        for k, v in self.order_data.items():
            if v > 0:
                print(f"{k}: {v}개, {v*self.cost[k]}원")
        total = sum(self.order_data[i] * self.cost[i] for i in self.items)
        print(f"Total: {total}원")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = TableOrderDemo()
    w.show()
    sys.exit(app.exec_())
