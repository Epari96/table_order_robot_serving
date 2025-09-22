#!/usr/bin/env python3
# dummy_nav2_server.py (ROS2 Humble)
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from nav2_msgs.action import NavigateToPose
from builtin_interfaces.msg import Duration
from geometry_msgs.msg import PoseStamped

class DummyNav2(Node):
    def __init__(self):
        super().__init__('dummy_nav2_server')
        self.declare_parameter('delay_sec', 5.0)

        self._cg = ReentrantCallbackGroup()
        self._preempt_seq = 0  # 선점 시퀀스(새 goal 수신 시 증가)

        # execute_callback 하나만 사용 (handle_accepted 없음)
        self._server = ActionServer(
            self,
            NavigateToPose,
            'navigate_to_pose',
            execute_callback=self.execute_cb,
            goal_callback=self.goal_cb,
            cancel_callback=self.cancel_cb,
            callback_group=self._cg,
        )
        self.get_logger().info('Dummy Nav2 started (preempt/cancel = CANCELED).')

    # 새 goal 수신 시: 선점 시퀀스 증가 -> 이전 execute 루프에서 감지하고 CANCELED 처리
    def goal_cb(self, _goal_req: NavigateToPose.Goal):
        self._preempt_seq += 1
        self.get_logger().info(f'Goal accepted (seq={self._preempt_seq}).')
        return GoalResponse.ACCEPT

    # 취소 요청은 수락만, 실제 상태 전이는 execute_cb에서 처리
    def cancel_cb(self, _goal_handle):
        return CancelResponse.ACCEPT

    def execute_cb(self, goal_handle):
        delay = float(self.get_parameter('delay_sec').value)
        my_seq = self._preempt_seq  # 이 goal이 시작될 때의 시퀀스 스냅샷

        # 로그(목표 좌표가 있으면 출력)
        try:
            p = goal_handle.request.pose.pose.position
            self.get_logger().info(f'Executing goal: x={p.x:.2f}, y={p.y:.2f} (seq={my_seq})')
        except Exception:
            self.get_logger().info(f'Executing goal (seq={my_seq}).')

        start = self.get_clock().now().nanoseconds / 1e9
        remaining = int(round(delay))
        while remaining > 0 and rclpy.ok():
            # 새 goal(선점) 또는 취소 요청 감지
            if self._preempt_seq != my_seq or goal_handle.is_cancel_requested:
                goal_handle.canceled()  # Nav2 규약: 선점/취소는 CANCELED
                self.get_logger().info(f'Goal canceled (preempt or client cancel, seq={my_seq} -> cur={self._preempt_seq}).')
                return NavigateToPose.Result()

            # 피드백
            fb = NavigateToPose.Feedback()
            if isinstance(goal_handle.request.pose, PoseStamped):
                fb.current_pose = goal_handle.request.pose
            elapsed = int(self.get_clock().now().nanoseconds / 1e9 - start)
            fb.navigation_time = Duration(sec=elapsed)
            fb.estimated_time_remaining = Duration(sec=max(0, remaining - 1))
            fb.distance_remaining = 0.0
            fb.number_of_recoveries = 0
            self.get_logger().info(f'Navigating... {remaining} sec left (seq={my_seq})')
            goal_handle.publish_feedback(fb)

            time.sleep(1.0)
            remaining -= 1

        # 완료 직전 한 번 더 확인
        if self._preempt_seq != my_seq or goal_handle.is_cancel_requested:
            goal_handle.canceled()
            self.get_logger().info(f'Goal canceled late (seq={my_seq} -> cur={self._preempt_seq}).')
            return NavigateToPose.Result()

        # 정상 완료
        goal_handle.succeed()
        self.get_logger().info(f'Goal succeeded (seq={my_seq}).')
        return NavigateToPose.Result()

def main():
    rclpy.init()
    node = DummyNav2()

    # MultiThreadedExecutor 로 취소/goal 서비스와 execute를 동시 처리
    execu = MultiThreadedExecutor(num_threads=2)
    execu.add_node(node)
    try:
        execu.spin()
    finally:
        execu.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
