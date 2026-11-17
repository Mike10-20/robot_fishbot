import rclpy
from rclpy.node import Node
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from rclpy.time import Time
class Mynode(Node):
    def __init__(self):
        super().__init__("tf_listener_py_node")
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        self.timer = self.create_timer(1.0,self.callback)
    def callback(self):
        if self.buffer.can_transform("camera","laser",Time()):
            tf = self.buffer.lookup_transform("camera","laser",Time())
            self.get_logger().info(f"frame-id{tf.header.frame_id},child-frame-id{tf.child_frame_id},({tf.transform.translation.x},{tf.transform.translation.y},{tf.transform.translation.z})")
        # else:
        #     try:
        #         self.buffer.lookup_transform("camera","laser",Time())
        #         tf = self.buffer.lookup_transform("camera","laser",Time())
        #         self.get_logger().info(f"frame-id{tf.header.frame_id},child-frame-id{tf.child_frame_id},({tf.transform.translation.x},{tf.transform.translation.y},{tf.transform.translation.z})")
        #     except Exception as e:
        #         self.get_logger().info(str(e))

def main():
    rclpy.init()
    rclpy.spin(Mynode())
    rclpy.shutdown()
            