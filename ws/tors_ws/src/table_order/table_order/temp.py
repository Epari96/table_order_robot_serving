import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import QTimer
import rclpy
from rclpy.executors import MultiThreadedExecutor
from git.ROKEY_Projects.advanced.table_order_robot_serving.ws.tors_ws.src.table_order.table_order.ros_node import ROSInterface
from queue import Queue
from threading import Thread

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROS2 PyQt GUI")
        self.resize(400, 300)

        # 레이아웃
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.input_order = QLineEdit()
        self.input_order.setPlaceholderText("Fibonacci order")
        self.layout.addWidget(self.input_order)

        self.send_button = QPushButton("Send Fibonacci Goal")
        self.layout.addWidget(self.send_button)

        self.pub_button = QPushButton("Publish Topic Message")
        self.layout.addWidget(self.pub_button)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        # GUI ↔ ROS 데이터 큐
        self.gui_queue = Queue()

        # ROS 초기화
        rclpy.init()
        self.ros_node = ROSInterface(self.gui_queue)

        # MultiThreadedExecutor로 ROS 콜백 실행
        self.executor = MultiThreadedExecutor()
        self.executor.add_node(self.ros_node)
        self.ros_thread = Thread(target=self.executor.spin, daemon=True)
        self.ros_thread.start()

        # 버튼 연결
        self.send_button.clicked.connect(self.send_goal)
        self.pub_button.clicked.connect(self.publish_message)

        # QTimer로 GUI 업데이트
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_text)
        self.timer.start(100)

    def send_goal(self):
        order_text = self.input_order.text()
        if order_text.isdigit():
            order = int(order_text)
            self.ros_node.send_fibonacci_goal(order)

    def publish_message(self):
        self.ros_node.publish_status("Hello from GUI!")

    def update_text(self):
        while not self.gui_queue.empty():
            msg = self.gui_queue.get()
            self.text_edit.append(msg)

    def closeEvent(self, event):
        self.executor.shutdown()
        rclpy.shutdown()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
