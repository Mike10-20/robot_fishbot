import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
class Mynode(Node):
    def __init__(self):
        super().__init__("tf_point_broadcaster_py_node")
        self.pub = self.create_publisher(PointStamped,"/point",10)
        self.timer = self.create_timer(1.0,self.callback)
        self.x = 0.0
    def callback(self):
        p = PointStamped()
        p.header.frame_id = "laser"
        p.header.stamp = self.get_clock().now().to_msg()
        p.point.x = self.x
        p.point.y = 0.0
        p.point.z = -1.0
        self.x += 0.05
        self.pub.publish(p)
def main():
    rclpy.init()
    rclpy.spin(Mynode())
    rclpy.shutdown()
