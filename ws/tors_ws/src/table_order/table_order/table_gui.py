#!/usr/bin/env python3
# table_client_gui.py
import sys, json, uuid
from PyQt5 import QtWidgets, QtCore

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from tors_interfaces.srv import OrderMsg  # ← 패키지명에 맞게 수정

# ----------------------------
# ROS 노드(서비스 클라이언트)
# ----------------------------
class OrderClientNode(Node):
    def __init__(self):
        super().__init__('table_order_client')
        self.cli = self.create_client(OrderMsg, '/pos/order_service')

    def wait_for_server(self, timeout_sec: float = 0.5) -> bool:
        return self.cli.wait_for_service(timeout_sec=timeout_sec)

    def call_order_async(self, table_id: str, client_order_id: str, items_json: str):
        req = OrderMsg.Request()
        req.table_id = table_id
        req.client_order_id = client_order_id
        req.items_json = items_json
        return self.cli.call_async(req)

# ----------------------------
# ROS 워커(QThread)
# ----------------------------
class RosWorker(QtCore.QThread):
    serviceResult = QtCore.pyqtSignal(bool, str)  # (accepted, message)
    rosLog = QtCore.pyqtSignal(str)

    @QtCore.pyqtSlot(str, str, str)
    def sendOrder(self, table_id: str, client_order_id: str, items_json: str):
        try:
            if not self.node.wait_for_server(timeout_sec=1.0):
                self.rosLog.emit('[ROS] 서비스 미가동: /pos/order_service')
                self.serviceResult.emit(False, 'POS 서비스 미가동')
                return

            future = self.node.call_order_async(table_id, client_order_id, items_json)

            def _done_cb(fut):
                accepted, message = False, '주문 거부'
                try:
                    resp = fut.result()  # OrderMsg.Response
                    accepted = bool(resp.accepted)
                    message = resp.message if resp.message else ('접수 완료' if accepted else '주문 거부')
                except Exception as e:
                    message = f'응답 오류: {e}'
                self.serviceResult.emit(accepted, message)

            future.add_done_callback(_done_cb)

        except Exception as e:
            self.rosLog.emit(f'[ROS] 서비스 호출 오류: {e}')
            self.serviceResult.emit(False, '주문 거부')

    def __init__(self):
        super().__init__()
        self.node = None
        self.exec = None

    def run(self):
        try:
            self.node = OrderClientNode()
            self.exec = MultiThreadedExecutor()
            self.exec.add_node(self.node)
            self.exec.spin()
        finally:
            try:
                if self.exec and self.node:
                    self.exec.remove_node(self.node)
                if self.node:
                    self.node.destroy_node()
            except Exception:
                pass

    def stop(self):
        try:
            if self.exec:
                self.exec.shutdown(timeout_sec=1.0)
        except Exception:
            pass
        self.quit()
        self.wait(1000)

# ----------------------------
# GUI
# ----------------------------
class ClientGUI(QtWidgets.QWidget):
    # GUI → ROS 스레드
    sendOrderSig = QtCore.pyqtSignal(str, str, str)

    def __init__(self, worker: RosWorker):
        super().__init__()
        self.setWindowTitle('Table Client (Service)')
        self.worker = worker

        # 위젯
        self.table_edit = QtWidgets.QLineEdit()
        self.table_edit.setPlaceholderText('예: T12')
        self.food_edit = QtWidgets.QLineEdit()
        self.food_edit.setPlaceholderText('음식명')
        self.qty_spin = QtWidgets.QSpinBox()
        self.qty_spin.setRange(1, 999)

        self.btn_send = QtWidgets.QPushButton('주문 전송')
        self.status_lbl = QtWidgets.QLabel('상태: 대기')
        self.log_view = QtWidgets.QPlainTextEdit(); self.log_view.setReadOnly(True)

        form = QtWidgets.QFormLayout()
        form.addRow('테이블 번호:', self.table_edit)
        form.addRow('음식명:', self.food_edit)
        form.addRow('수량:', self.qty_spin)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.btn_send)
        layout.addWidget(self.status_lbl)
        layout.addWidget(self.log_view)

        # 시그널 연결
        self.btn_send.clicked.connect(self.on_send_clicked)
        self.sendOrderSig.connect(self.worker.sendOrder)
        self.worker.serviceResult.connect(self.on_service_result)

    def on_send_clicked(self):
        table_id = self.table_edit.text().strip()
        food = self.food_edit.text().strip()
        qty = int(self.qty_spin.value())

        if not table_id:
            self.status_lbl.setText('상태: 테이블 번호 입력')
            return
        if not food:
            self.status_lbl.setText('상태: 음식명 입력')
            return

        client_order_id = str(uuid.uuid4())
        items_json = json.dumps({food: qty}, ensure_ascii=False)

        self.status_lbl.setText('상태: 주문 전송중')
        self.log_view.appendPlainText(f'[GUI] 요청 → table={table_id}, uuid={client_order_id}, items={items_json}')
        self.sendOrderSig.emit(table_id, client_order_id, items_json)

    @QtCore.pyqtSlot(bool, str)
    def on_service_result(self, accepted: bool, message: str):
        self.status_lbl.setText(f'상태: {"접수 완료" if accepted else "주문 거부"}')
        self.log_view.appendPlainText(f'[GUI] 응답 ← {message}')

def main():
    rclpy.init()
    app = QtWidgets.QApplication(sys.argv)

    worker = RosWorker()
    worker.start()

    w = ClientGUI(worker)
    w.resize(460, 300)
    w.show()

    code = app.exec_()
    worker.stop()
    rclpy.shutdown()
    sys.exit(code)

if __name__ == '__main__':
    main()
