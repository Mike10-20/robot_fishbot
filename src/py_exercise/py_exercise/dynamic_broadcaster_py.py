import rclpy
from rclpy.node import Node
from tf2_ros.transform_broadcaster import TransformBroadcaster
import tf_transformations
from turtlesim.msg import Pose
from geometry_msgs.msg import TransformStamped
class Mynode(Node):
    def __init__(self):
        super().__init__("broadcaster_py_node")
        self.declare_parameter("frame-id","world")
        self.declare_parameter("child-frame-id","turtle1")
        self.father = self.get_parameter("frame-id").get_parameter_value().string_value
        self.child = self.get_parameter("child-frame-id").get_parameter_value().string_value
        self.sub = self.create_subscription(Pose,"/"+self.child+"/pose",self.callback,10)
        self.broadcaster = TransformBroadcaster(self)
    def callback(self,msg):
        tf = TransformStamped()
        tf.header.stamp = self.get_clock().now().to_msg()
        tf.header.frame_id = self.father
        tf.child_frame_id = self.child
        tf.transform.translation.x = msg.x
        tf.transform.translation.y = msg.y
        tf.transform.translation.z = 0.0
        qt = tf_transformations.quaternion_from_euler(0.0,0.0,msg.theta)
        tf.transform.rotation.x = qt[0]
        tf.transform.rotation.y = qt[1]
        tf.transform.rotation.z = qt[2]
        tf.transform.rotation.w = qt[3]
        self.broadcaster.sendTransform(tf)
def main():
    rclpy.init()
    rclpy.spin(Mynode())
    rclpy.shutdown()




