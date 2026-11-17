import rclpy
from rclpy.node import Node
from rclpy.logging import get_logger
from geometry_msgs.msg import TransformStamped
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
import tf_transformations
import sys
class Mynode(Node):
    def __init__(self,argv):
        super().__init__("static_tf_broadcaster_py_node")
        self.broadcaster = StaticTransformBroadcaster(self)
        self.send_tf(argv)
    def send_tf(self,argv):
        tf = TransformStamped()
        tf.header.stamp = self.get_clock().now().to_msg()
        tf.header.frame_id = argv[7]
        tf.child_frame_id = argv[8]
        qt = tf_transformations.quaternion_from_euler(float(argv[4]),float(argv[5]),float(argv[6]))
        tf.transform.translation.x = float(argv[1])
        tf.transform.translation.y = float(argv[2])
        tf.transform.translation.z = float(argv[3])
        tf.transform.rotation.x = qt[0]
        tf.transform.rotation.y = qt[1]
        tf.transform.rotation.z = qt[2]
        tf.transform.rotation.w = qt[3]
        self.broadcaster.sendTransform(tf)
def main():
    if len(sys.argv)!=9:
        get_logger("rclpy").error("please input 8 parameters")
        return
    rclpy.init()
    node = Mynode(sys.argv)
    rclpy.spin(node)
    rclpy.shutdown()






