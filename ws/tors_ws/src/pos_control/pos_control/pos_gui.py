#!/usr/bin/env python3
# pos_server_gui.py
import sys, json, uuid, threading, time
from typing import Optional, Dict
from PyQt5 import QtWidgets, QtCore

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from tors_interfaces.srv import OrderMsg  # ← 패키지명에 맞게 수정

# ----------------------------
# ROS 노드(서비스 서버)
# ----------------------------
class PosServerNode(Node):
    def __init__(self, decide_fn, timeout_sec: float = 30.0):
        super().__init__('pos_server_gui')
        self.timeout_sec = timeout_sec
        self.decide_fn = decide_fn  # (client_order_id) -> (accepted: Optional[bool], message: str)
        self.srv = self.create_service(OrderMsg, '/pos/order_service', self.on_order)

    def on_order(self, req: OrderMsg.Request, resp: OrderMsg.Response):
        # GUI에 표시하기 쉽게 dict로 파싱
        try:
            items = json.loads(req.items_json) if req.items_json else {}
        except Exception:
            items = {'_parse_error': req.items_json}

        # GUI에게 알리고 결정 기다리기
        accepted, message = self.decide_fn(req.table_id, req.client_order_id, items, self.timeout_sec)

        if accepted is None:
            # 타임아웃 등으로 미결정 → 자동 거절
            accepted = False
            message = '응답 시간 초과로 주문 거부'

        # 서버 발급 order_id (예시)
        order_id = f'ORD-{uuid.uuid4().hex[:8].upper()}'

        resp.accepted = bool(accepted)
        resp.order_id = order_id
        resp.message = message or ('접수 완료' if accepted else '주문 거부')

        self.get_logger().info(
            f'order_decision: table={req.table_id} uuid={req.client_order_id} '
            f'accepted={resp.accepted} order_id={resp.order_id} msg="{resp.message}"'
        )
        return resp

# ----------------------------
# ROS 워커(QThread)
# ----------------------------
class RosWorker(QtCore.QThread):
    # GUI로 요청 표시
    newRequest = QtCore.pyqtSignal(str, str, str)  # table_id, client_order_id, items_pretty

    def __init__(self, decide_proxy):
        super().__init__()
        self.node = None
        self.exec = None
        self.decide_proxy = decide_proxy  # GUI의 결정 메서드(스레드 안전)

    def run(self):
        try:
            self.node = PosServerNode(self.decide_proxy)
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
class ServerGUI(QtWidgets.QWidget):
    # 서버 콜백 ↔ GUI 간 동기화용 (client_order_id → Event/결정값)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('POS Server (Service)')

        # 현재 대기 중인 요청 상태
        self._lock = threading.Lock()
        self._waiting_event: Optional[threading.Event] = None
        self._waiting_uuid: Optional[str] = None
        self._decision: Optional[bool] = None
        self._message: str = ''

        # 위젯
        self.info = QtWidgets.QPlainTextEdit(); self.info.setReadOnly(True)
        self.btn_accept = QtWidgets.QPushButton('수락')
        self.btn_reject = QtWidgets.QPushButton('거절')
        self.status = QtWidgets.QLabel('상태: 대기')

        btns = QtWidgets.QHBoxLayout()
        btns.addWidget(self.btn_accept)
        btns.addWidget(self.btn_reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel('들어온 주문'))
        layout.addWidget(self.info)
        layout.addLayout(btns)
        layout.addWidget(self.status)

        self.btn_accept.clicked.connect(lambda: self._set_decision(True, '접수 완료'))
        self.btn_reject.clicked.connect(lambda: self._set_decision(False, '주문 거부'))

        # ROS 워커 생성 (decide_proxy를 넘김)
        self.worker = RosWorker(self._decide_proxy)
        self.worker.start()

    # 서버 콜백이 호출하는 결정 함수
    def _decide_proxy(self, table_id: str, client_order_id: str, items: Dict, timeout_sec: float):
        # 요청 내용을 GUI에 보여주고 응답 대기
        pretty = json.dumps(items, ensure_ascii=False, indent=2)
        QtCore.QMetaObject.invokeMethod(
            self, '_show_request', QtCore.Qt.QueuedConnection,
            QtCore.Q_ARG(str, table_id),
            QtCore.Q_ARG(str, client_order_id),
            QtCore.Q_ARG(str, pretty)
        )

        ev = threading.Event()
        with self._lock:
            self._waiting_event = ev
            self._waiting_uuid = client_order_id
            self._decision = None
            self._message = ''

        decided = ev.wait(timeout=timeout_sec)
        with self._lock:
            decision = self._decision
            message = self._message
            # 클리어
            self._waiting_event = None
            self._waiting_uuid = None
            self._decision = None
            self._message = ''
        return (decision if decided else None, message)

    @QtCore.pyqtSlot(str, str, str)
    def _show_request(self, table_id: str, client_order_id: str, items_pretty: str):
        self.info.setPlainText(
            f'테이블: {table_id}\n'
            f'UUID: {client_order_id}\n'
            f'항목:\n{items_pretty}'
        )
        self.status.setText('상태: 응답 대기')

    def _set_decision(self, accepted: bool, message: str):
        with self._lock:
            if not self._waiting_event:
                self.status.setText('상태: 대기 (결정할 요청 없음)')
                return
            self._decision = accepted
            self._message = message
            self._waiting_event.set()
        self.status.setText(f'상태: {"수락" if accepted else "거절"} 처리')

    def closeEvent(self, e):
        try:
            self.worker.stop()
        finally:
            e.accept()

def main():
    rclpy.init()
    app = QtWidgets.QApplication(sys.argv)

    w = ServerGUI()
    w.resize(520, 420)
    w.show()

    code = app.exec_()
    rclpy.shutdown()
    sys.exit(code)

if __name__ == '__main__':
    main()
