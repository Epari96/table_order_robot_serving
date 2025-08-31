import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from example_interfaces.action import Fibonacci
from std_msgs.msg import String
from threading import Thread
from queue import Queue

class ROSInterface(Node):
    def __init__(self, gui_queue):
        super().__init__('ros_interface')
        self.gui_queue = gui_queue

        # 액션 클라이언트
        self.action_client = ActionClient(self, Fibonacci, 'fibonacci')

        # 퍼블리셔
        self.pub = self.create_publisher(String, 'status', 10)

        # 구독
        self.sub = self.create_subscription(String, 'status', self.topic_callback, 10)

    def send_fibonacci_goal(self, order):
        self.get_logger().info(f"Sending Fibonacci goal: {order}")
        goal_msg = Fibonacci.Goal(order=order)

        self.action_client.wait_for_server()

        send_goal_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected :(")
            return
        self.get_logger().info("Goal accepted :)")
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback.sequence
        # GUI 업데이트용 큐에 전달
        self.gui_queue.put(f"Feedback: {feedback}")

    def result_callback(self, result_future):
        result = result_future.result().result.sequence
        self.gui_queue.put(f"Result: {result}")
        self.get_logger().info(f"Result: {result}")

    def topic_callback(self, msg):
        self.gui_queue.put(f"Topic: {msg.data}")

    def publish_status(self, data):
        msg = String()
        msg.data = data
        self.pub.publish(msg)
