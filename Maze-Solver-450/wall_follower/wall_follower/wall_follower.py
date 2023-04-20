"""
    Minimal code for wall follower 
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy
from rclpy.qos import QoSProfile
from sensor_msgs.msg import LaserScan

class Follow(Node):
    def __init__(self):
        super().__init__('follow')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = QoSReliabilityPolicy.BEST_EFFORT
        qos_profile.durability = QoSDurabilityPolicy.VOLATILE
        self.subscription= self.create_subscription(
            LaserScan,
            '/scan',  ## Read
            self.listener_callback,
            qos_profile,
        )
        timer_period = 0.5  # seconds
        self.i = 0
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        
    def getch(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    def timer_callback(self):
        '''
        Publisher callback function
        TODO: implement
        '''
        msg = Twist()
        key = self.getch()
        if key == 'm':
            msg.linear.x = 0.5 
        elif key == 'b':
            msg.linear.x = -0.5
        elif key == 'c':
            msg.linear.x = 0.0
        self.publisher_.publish(msg)
        
    def listener_callback(self,msg):
        '''
        Subscription Callback 
        TODO: implement
        '''
        self.get_logger().info('I hear something: 0 deg "%f" 90 deg "%f" 180 deg "%f" 270 deg "%f"' %(msg.ranges[0], msg.ranges[190], msg.ranges[380], msg.ranges[570]))
        # self.get_logger().info(str(len(msg.ranges)))
        # self.get_logger().info("a")

def main(args=None):
    rclpy.init(args=args)
    my_follower = Follow()
    rclpy.spin(my_follower)
    my_follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()