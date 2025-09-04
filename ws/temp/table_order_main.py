# main.py
import sys
from PyQt5 import QtWidgets
from menu_item_widget import TableOrderWindow

def on_waiter():
    print("[CALLBACK] 직원 호출 (ROS2 pub 자리)")

def on_confirm():
    print("[CALLBACK] 수령완료 (ROS2 service 자리)")

def on_order(win: TableOrderWindow):
    print("[CALLBACK] 주문 확정")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = TableOrderWindow()
    w.waiterClicked.connect(on_waiter)
    w.confirmReceiptClicked.connect(on_confirm)
    w.orderClicked.connect(lambda: on_order(w))
    w.show()
    sys.exit(app.exec_())
