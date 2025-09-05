import sys, math, json, os
from PyQt5 import QtWidgets, QtCore
from geometry_msgs.msg import PoseStamped, Twist
from rclpy.action import ActionClient
from ament_index_python.packages import get_package_share_directory

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from nav2_msgs.action import NavigateToPose
from std_msgs.msg import Int32, Bool

from tors_interfaces.srv import OrderMsg
from pos_control.pos_gui_widget import PosGuiWidget

share = get_package_share_directory('pos_control')
UI_PATH = os.environ.get('POS_CONTROL_UI', os.path.join(share, 'resource', 'PosControl.ui'))
DB_PATH = "pos_orders.db"

NAV_ACTION_NAME = "/navigate_to_pose"
CMD_VEL_TOPIC   = "/cmd_vel"
ORDER_SERVICE_NAME = "/pos/order_service"
CALL_WAITER_TOPIC  = "/pos/call_waiter"        # Int32(table_no)
CONFIRM_RECEIPT_TOPIC = "/pos/confirm_receipt" # Bool

NAV_POINTS = {
    "tables": { 1:(1.0,2.0,0.0), 2:(2.0,2.0,0.0), 3:(3.0,2.0,0.0),
                4:(1.0,3.0,math.pi/2), 5:(2.0,3.0,math.pi/2), 6:(3.0,3.0,math.pi/2) },
    "call":   (0.0, 0.0, 0.0),
    "charge": (-1.0, -1.0, 0.0),
}

def yaw_to_quat(yaw: float):
    cz = math.cos(yaw * 0.5); sz = math.sin(yaw * 0.5)
    return (0.0, 0.0, sz, cz)

class RosWorker(QtCore.QThread):
    # ROS -> GUI
    navStatus       = QtCore.pyqtSignal(str, str)       # (status, location_key)
    orderRequest    = QtCore.pyqtSignal(int, str, str)  # (table_id, client_order_id, items_json)
    waiterCall      = QtCore.pyqtSignal(int)
    confirmReceipt  = QtCore.pyqtSignal(bool)

    # GUI -> ROS
    @QtCore.pyqtSlot(str, float, float, float)
    def send_nav_goal(self, location_key: str, x: float, y: float, yaw: float):
        if not self._action_client.wait_for_server(timeout_sec=2.0):
            self.node.get_logger().error("Nav2 action server not available."); return
        with self._goal_lock:
            if self._current_goal_handle is not None:
                try: self._action_client._cancel_goal_async(self._current_goal_handle)
                except Exception: pass

            ps = PoseStamped(); ps.header.frame_id = "map"; ps.header.stamp = self.node.get_clock().now().to_msg()
            ps.pose.position.x = float(x); ps.pose.position.y = float(y)
            qx,qy,qz,qw = yaw_to_quat(yaw)
            ps.pose.orientation.x, ps.pose.orientation.y, ps.pose.orientation.z, ps.pose.orientation.w = qx,qy,qz,qw
            goal_msg = NavigateToPose.Goal(); goal_msg.pose = ps

            send_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self._on_nav_feedback)
            def _on_goal_response(fut):
                try: gh = fut.result()
                except Exception as e:
                    self.node.get_logger().error(f"send_goal failed: {e}"); return
                if not gh.accepted:
                    self.node.get_logger().warn("Goal rejected."); self.navStatus.emit("stopped", location_key); return
                with self._goal_lock:
                    self._current_goal_handle = gh; self._current_goal_key = location_key
                self.navStatus.emit("moving", location_key)
                result_future = gh.get_result_async()
                result_future.add_done_callback(lambda f: self._on_nav_result(location_key, f))
            send_future.add_done_callback(_on_goal_response)

    @QtCore.pyqtSlot()
    def cancel_all_goals(self):
        with self._goal_lock:
            try:
                if self._current_goal_handle is not None:
                    self._action_client._cancel_goal_async(self._current_goal_handle)
            except Exception: pass

    @QtCore.pyqtSlot(float)
    def publish_zero_twist_for(self, seconds: float = 0.7):
        twist = Twist()
        end_time = self.node.get_clock().now().nanoseconds + int(seconds * 1e9)
        rate = self.node.create_rate(20.0)
        while self.node.get_clock().now().nanoseconds < end_time:
            self._cmd_pub.publish(twist); rate.sleep()

    @QtCore.pyqtSlot(str, bool)
    def set_order_decision(self, client_order_id: str, accepted: bool):
        tup = self._pending_order.get(client_order_id)
        if tup:
            ev, holder = tup
            holder["accepted"] = bool(accepted); ev.set()

    def run(self):
        import threading
        rclpy.init()
        self.node = Node("pos_control")
        self._executor = MultiThreadedExecutor(); self._executor.add_node(self.node)

        self._action_client = ActionClient(self.node, NavigateToPose, NAV_ACTION_NAME)
        self._cmd_pub = self.node.create_publisher(Twist, CMD_VEL_TOPIC, 10)

        self._srv = self.node.create_service(OrderMsg, ORDER_SERVICE_NAME, self._on_order_service)
        self._sub_call = self.node.create_subscription(Int32, CALL_WAITER_TOPIC, self._on_waiter_call, 10)
        self._sub_confirm = self.node.create_subscription(Bool, CONFIRM_RECEIPT_TOPIC, self._on_confirm_receipt, 10)

        self._goal_lock = threading.Lock()
        self._current_goal_handle = None; self._current_goal_key = None
        self._pending_order = {}

        try: self._executor.spin()
        finally:
            self._executor.shutdown(); self.node.destroy_node(); rclpy.shutdown()

    # --- callbacks ---
    def _on_nav_feedback(self, feedback_msg): pass

    def _on_nav_result(self, location_key: str, fut):
        try: res = fut.result(); status = res.status
        except Exception as e:
            self.node.get_logger().error(f"get_result failed: {e}"); status = 0
        if status == 4: self.navStatus.emit("arrived", location_key)
        elif status == 2: self.navStatus.emit("cancelled", location_key)
        elif status == 5: self.navStatus.emit("aborted", location_key)
        else: self.navStatus.emit("stopped", location_key)
        self._current_goal_handle = None; self._current_goal_key = None

    def _on_order_service(self, req: OrderMsg.Request, res: OrderMsg.Response):
        import threading
        # req.table_id: int, req.items: OrderItem[]
        try:
            items_dict = {getattr(it, 'name',''): int(getattr(it, 'quantity',0))
                          for it in req.items if getattr(it,'name','')}
        except Exception:
            items_dict = {}
            for it in getattr(req, 'items', []):
                n = getattr(it,'name',''); q = getattr(it,'quantity',0)
                if n: items_dict[n] = int(q) if isinstance(q,(int,float)) else 0
        items_json = json.dumps(items_dict, ensure_ascii=False)

        ev = threading.Event(); holder = {"accepted": False}
        self._pending_order[req.client_order_id] = (ev, holder)
        # emit with int table_id
        self.orderRequest.emit(int(req.table_id), req.client_order_id, items_json)
        ev.wait(timeout=120.0)
        res.accepted = bool(holder["accepted"])
        try: res.message = 'accepted' if res.accepted else 'rejected'
        except Exception: pass
        self._pending_order.pop(req.client_order_id, None)
        return res

    def _on_waiter_call(self, msg: Int32):
        self.waiterCall.emit(int(msg.data))

    def _on_confirm_receipt(self, msg: Bool):
        self.confirmReceipt.emit(bool(msg.data))

def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = PosGuiWidget(UI_PATH, NAV_POINTS, DB_PATH)

    worker = RosWorker()
    # GUI -> ROS
    gui.requestNavGoal.connect(worker.send_nav_goal)
    gui.requestCancel.connect(worker.cancel_all_goals)
    gui.requestZeroTwist.connect(worker.publish_zero_twist_for)
    gui.orderDecision.connect(worker.set_order_decision)
    # ROS -> GUI
    worker.navStatus.connect(gui.on_nav_status)
    worker.orderRequest.connect(gui.on_order_request_popup)
    worker.waiterCall.connect(gui.on_waiter_call)
    worker.confirmReceipt.connect(gui.on_confirm_receipt)

    worker.start(); gui.show()
    rc = app.exec_()
    if worker.isRunning():
        try: worker._executor.shutdown()
        except Exception: pass
    sys.exit(rc)

if __name__ == "__main__":
    main()
