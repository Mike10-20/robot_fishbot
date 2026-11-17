import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import tf_transformations
from rclpy.time import Time
class Mynode(Node):
    def __init__(self):
        super().__init__("dynamic_tf_listener_py_node")
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        self.timer = self.create_timer(1,self.callback)
    def callback(self):
        if self.buffer.can_transform("map","base_footprint",Time()):
            tf = self.buffer.lookup_transform("map","base_footprint",Time())
            e = tf_transformations.euler_from_quaternion([tf.transform.rotation.x,tf.transform.rotation.y,tf.transform.rotation.z,tf.transform.rotation.w])
            self.get_logger().info("(%.2f,%.2f),%.2f" % (tf.transform.translation.x,tf.transform.translation.y,e[2]))
def main():
    rclpy.init()
    node = Mynode()
    rclpy.spin(node)
    rclpy.shutdown()