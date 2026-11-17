import rclpy
from rclpy.node import Node
from tf2_ros.transform_listener import TransformListener
from tf2_ros.buffer import Buffer
from geometry_msgs.msg import Twist
from rclpy.time import Time
import math
class Mynode(Node):
    def __init__(self):
        super().__init__("listener_py_node")
        self.declare_parameter("father","t2")
        self.declare_parameter("child","turtle1")
        self.father = self.get_parameter("father").get_parameter_value().string_value
        self.child = self.get_parameter("child").get_parameter_value().string_value
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        self.pub = self.create_publisher(Twist,"/"+self.father+"/cmd_vel",10)
        self.timer = self.create_timer(1.0,self.callback)
    def callback(self):
        if self.buffer.can_transform(self.father,self.child,Time()):
            tf = self.buffer.lookup_transform(self.father,self.child,Time())
            tw = Twist()
            x = tf.transform.translation.x
            y = tf.transform.translation.y
            x_vel = 0.5*math.sqrt(math.pow(x,2)+math.pow(y,2))
            yaw_vel = 1*math.atan2(y,x)
            tw.linear.x = x_vel 
            tw.angular.z = yaw_vel
            self.pub.publish(tw)
def main():
    rclpy.init()
    rclpy.spin(Mynode())
    rclpy.shutdown()



