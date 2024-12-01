import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import threading
import time

class TeleopController(Node):
    def __init__(self):
        super().__init__('teleop_controller')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Movement settings
        self.linear_speed = 1.0  # meters per second
        self.angular_speed = 2.5  # radians per second
        
        print("""
Control Your Robot!
------------------
Moving around:
   w
a  s  d

w/s : forward/backward
a/d : rotate left/right
x : stop
q : quit

Press keys in this terminal to control the robot.
""")
        
        # Start keyboard reading thread
        self.thread = threading.Thread(target=self.read_keyboard)
        self.thread.daemon = True
        self.thread.start()

    def read_keyboard(self):
        while True:
            # Read a single character
            key = input().lower()
            
            # Create Twist message
            twist = Twist()
            
            # Set velocity based on key
            if key == 'w':
                twist.linear.x = self.linear_speed
                self.get_logger().info('Moving forward')
            elif key == 's':
                twist.linear.x = -self.linear_speed
                self.get_logger().info('Moving backward')
            elif key == 'a':
                twist.angular.z = self.angular_speed
                self.get_logger().info('Turning left')
            elif key == 'd':
                twist.angular.z = -self.angular_speed
                self.get_logger().info('Turning right')
            elif key == 'x':
                # Stop
                self.get_logger().info('Stopping')
            elif key == 'q':
                self.get_logger().info('Quitting...')
                sys.exit(0)
            
            # Publish the movement command
            self.publisher.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    controller = TeleopController()
    
    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        print("\nShutting down teleop node...")
    finally:
        # Stop the robot before shutting down
        twist = Twist()
        controller.publisher.publish(twist)
        controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()