#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtWidgets, QtCore

from table_order.table_gui_widget import TableOrderWindow

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from std_msgs.msg import Int32
from std_srvs.srv import SetBool
from tors_interfaces.srv import OrderMsg
import json

class TableClientNode(Node):
    def __init__(self,
                 waiter_topic: str = '/pos/call_waiter',
                 confirm_srv: str = '/pos/confirm_receipt',
                 order_srv: str = '/pos/order_service'):
        super().__init__('table_order_client')
        self.waiter_pub = self.create_publisher(Int32, waiter_topic, 10)
        self.confirm_cli = self.create_client(SetBool, confirm_srv)
        self.order_cli   = self.create_client(OrderMsg, order_srv)

class RosWorker(QtCore.QThread):
    orderResult   = QtCore.pyqtSignal(bool, str)
    confirmResult = QtCore.pyqtSignal(bool, str)
    rosLog        = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.node: TableClientNode | None = None
        self.exec: MultiThreadedExecutor | None = None

    def _emit_log(self, msg: str): self.rosLog.emit(msg)

    def _safe_service(self, wait_fn, call_future_fn, done_handler, wait_timeout=1.0, name='service'):
        try:
            if not wait_fn(timeout_sec=wait_timeout):
                self._emit_log(f'[ROS] 서비스 미가동: {name}')
                done_handler(None, exc=RuntimeError('service unavailable')); return
            fut = call_future_fn()
            def _cb(f):
                try:    resp = f.result(); done_handler(resp, exc=None)
                except Exception as e: done_handler(None, exc=e)
            fut.add_done_callback(_cb)
        except Exception as e:
            done_handler(None, exc=e)

    @QtCore.pyqtSlot(int)
    def sendWaiter(self, table_no: int):
        if not self.node: return
        try:
            self.node.waiter_pub.publish(Int32(data=int(table_no)))
            self._emit_log(f'[ROS] 직원 호출: table={table_no}')
        except Exception as e:
            self._emit_log(f'[ROS] 퍼블리시 오류: {e}')

    @QtCore.pyqtSlot()
    def sendConfirm(self):
        if not self.node: return
        self._safe_service(
            wait_fn=self.node.confirm_cli.wait_for_service,
            call_future_fn=lambda: self.node.confirm_cli.call_async(SetBool.Request(data=True)),
            done_handler=lambda resp, exc: (
                self.confirmResult.emit(bool(getattr(resp,'success',False)),
                                        getattr(resp,'message','성공' if getattr(resp,'success',False) else '실패'))
                if exc is None else self.confirmResult.emit(False, f'오류: {exc}')
            ),
            name='/pos/confirm_receipt'
        )

    @QtCore.pyqtSlot(int, str, object)
    def sendOrder(self, table_id: int, client_order_id: str, items_dict: dict):
        if not self.node: return
        req = OrderMsg.Request()
        req.table_id = int(table_id)
        req.client_order_id = client_order_id
        # JSON 문자열로 인코딩해서 전송
        req.items_json = json.dumps(
            {k:int(v) for k,v in items_dict.items() if int(v) > 0},
            ensure_ascii=False
        )

        self._safe_service(
            wait_fn=self.node.order_cli.wait_for_service,
            call_future_fn=lambda: self.node.order_cli.call_async(req),
            done_handler=lambda resp, exc: (
                self.orderResult.emit(bool(getattr(resp,'accepted',False)),
                                      getattr(resp,'message','접수 완료' if getattr(resp,'accepted',False) else '주문 거부'))
                if exc is None else self.orderResult.emit(False, f'오류: {exc}')
            ),
            name='/pos/order_service'
        )

    def run(self):
        try:
            self.node = TableClientNode()
            self.exec = MultiThreadedExecutor(); self.exec.add_node(self.node); self.exec.spin()
        finally:
            try:
                if self.exec and self.node: self.exec.remove_node(self.node)
                if self.node: self.node.destroy_node()
            except Exception: pass

    def stop(self):
        try:
            if self.exec: self.exec.shutdown(timeout_sec=1.0)
        except Exception: pass
        self.quit(); self.wait(1000)

def main():
    rclpy.init()
    app = QtWidgets.QApplication(sys.argv)

    worker = RosWorker(); worker.start()
    w = TableOrderWindow(); w.resize(1000, 600)

    # GUI -> ROS
    w.waiterClicked.connect(worker.sendWaiter)
    w.confirmReceiptClicked.connect(worker.sendConfirm)
    w.orderPayload.connect(worker.sendOrder)

    # 로그 -> 수락 / 거부 결과 전송
    worker.orderResult.connect(lambda ok,msg: print(f"[ORDER] {'OK' if ok else 'FAIL'}: {msg}"))
    worker.confirmResult.connect(lambda ok,msg: print(f"[CONFIRM] {'OK' if ok else 'FAIL'}: {msg}"))
    worker.rosLog.connect(lambda s: print(s))

    # 주문 결과를 테이블 팝업 상태로 반영
    def _map_order_result(ok: bool, msg: str):
        # 예외/서비스 미가동 등은 'failed', 그 외 False는 'rejected'
        status = "accepted" if ok else ("failed" if msg.startswith("오류:") or "미가동" in msg else "rejected")
        w.finalize_order(status)

    worker.orderResult.connect(_map_order_result)

    w.show(); code = app.exec_()
    worker.stop(); rclpy.shutdown(); sys.exit(code)

if __name__ == '__main__':
    main()
