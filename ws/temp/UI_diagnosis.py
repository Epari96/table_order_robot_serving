# debug_ui_names.py
from PyQt5 import QtWidgets, uic
import sys
UI = "PosControl.ui"  # 절대경로 가능

app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QMainWindow()
uic.loadUi(UI, w)

btns = w.findChildren(QtWidgets.QPushButton)
txts = w.findChildren(QtWidgets.QTextEdit)

print("== Control Buttons (btnCtrlTable*) ==")
for b in sorted([b for b in btns if b.objectName().startswith("btnCtrlTable")], key=lambda x: x.objectName()):
    print(" ", b.objectName())

print("== Status Buttons (btnTable*) ==")
for b in sorted([b for b in btns if b.objectName().startswith("btnTable")], key=lambda x: x.objectName()):
    print(" ", b.objectName())

print("== Required ==")
need = ["btnRobot1","btnRobot2","btnCallRobot","btnGoCharge","btnEStop","btnPayment","btnSales","txtOrderLog"]
have = {b.objectName() for b in btns} | {t.objectName() for t in txts}
missing = [n for n in need if n not in have]
print(" Missing:", missing if missing else "(none)")
