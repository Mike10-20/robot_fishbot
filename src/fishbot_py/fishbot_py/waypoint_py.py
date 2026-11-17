from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
from rclpy.duration import Duration
import rclpy
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
    way_point = []
    pose1 = PoseStamped()
    pose1.header.stamp = navigator.get_clock().now().to_msg()
    pose1.header.frame_id = "map"
    pose1.pose.position.x = 1.0
    pose1.pose.position.y = 0.0
    pose1.pose.orientation.w = 1.0
    way_point.append(pose1)
    pose2 = PoseStamped()
    pose2.header.stamp = navigator.get_clock().now().to_msg()
    pose2.header.frame_id = "map"
    pose2.pose.position.x = 2.0
    pose2.pose.position.y = 0.0
    pose2.pose.orientation.w = 1.0
    way_point.append(pose2)
    pose3 = PoseStamped()
    pose3.header.stamp = navigator.get_clock().now().to_msg()
    pose3.header.frame_id = "map"
    pose3.pose.position.x = 3.0
    pose3.pose.position.y = 3.0
    pose3.pose.orientation.w = 1.0
    way_point.append(pose3)
    navigator.followWaypoints(way_point)
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        navigator.get_logger().info(f"ongoing task:{feedback.current_waypoint +1}")
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        navigator.get_logger().info("navigate succeed")
    elif result == TaskResult.CANCELED:
        navigator.get_logger().info("navigate be canceled")
    elif result == TaskResult.FAILED:
        navigator.get_logger().info("navigate is failed")
    else:
        navigator.get_logger().info("navigate is unknowed")
    rclpy.spin(navigator)
    rclpy.shutdown()
         




