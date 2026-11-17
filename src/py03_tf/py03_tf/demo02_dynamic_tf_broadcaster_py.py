import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from turtlesim.msg import Pose
from tf2_ros.transform_broadcaster import TransformBroadcaster
from tf_transformations import quaternion_from_euler
class Mynode(Node):
    def __init__(self):
        super().__init__("dynamic_tf_broadcaster_py_node")
        self.sub = self.create_subscription(Pose,"/turtle1/pose",self.callback,10)
        self.broadcaster = TransformBroadcaster(self)
    def callback(self,msg):
        tf = TransformStamped()
        tf.header.frame_id = "world"
        tf.header.stamp = self.get_clock().now().to_msg()
        tf.child_frame_id = "turtle1"
        tf.transform.translation.x = msg.x
        tf.transform.translation.y = msg.y
        tf.transform.translation.z = 0.0
        qt = quaternion_from_euler(0.0,0.0,msg.theta)
        tf.transform.rotation.x = qt[0]
        tf.transform.rotation.y = qt[1]
        tf.transform.rotation.z = qt[2]
        tf.transform.rotation.w = qt[3]
        self.broadcaster.sendTransform(tf)
def main():
    rclpy.init()
    node = Mynode()
    rclpy.spin(node)
    rclpy.shutdown()


