from geometry_msgs.msg import PoseStamped
import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
def main():
    rclpy.init()
    navigator = BasicNavigator()
    pose = PoseStamped()
    pose.header.frame_id="map"
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = 0.0
    pose.pose.position.y = 0.0
    pose.pose.position.z = 0.0
    pose.pose.orientation.w = 1.0
    navigator.setInitialPose(pose)
    navigator.waitUntilNav2Active()
    rclpy.spin(navigator)
    rclpy.shutdown()

