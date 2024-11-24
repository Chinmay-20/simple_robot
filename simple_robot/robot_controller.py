import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_robot)
        self.direction = 1  # 1 for forward, -1 for backward
        self.switch_time = time.time() + 3.0  # Switch direction every 3 seconds

    def move_robot(self):
        current_time = time.time()
        
        # Switch direction every 3 seconds
        if current_time > self.switch_time:
            self.direction *= -1  # Reverse direction
            self.switch_time = current_time + 3.0
        
        # Create and publish movement command
        twist = Twist()
        twist.linear.x = 0.5 * self.direction  # Move at 0.5 m/s
        twist.angular.z = 0.0
        self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    controller = RobotController()
    rclpy.spin(controller)
    controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()