import sys
from PyQt5 import QtWidgets, uic

class TableOrderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # table_order.ui 파일을 로드
        uic.loadUi("PosControl.ui", self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TableOrderApp()
    window.show()
    sys.exit(app.exec_())
