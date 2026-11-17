from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
import rclpy
from tf2_ros.transform_listener import TransformListener
from tf2_ros.buffer import Buffer
import tf_transformations
from rclpy.duration import Duration
from rclpy.time import Time
from autopatrol_interface.srv import Speech
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class Mynode(BasicNavigator):
    def __init__(self):
        super().__init__("patrol_node")
        self.declare_parameter("initial_point",[0.0,0.0,0.0])
        self.declare_parameter("target_points",[1.0,0.0,0.0,1.0,1.0,1.57])
        self.declare_parameter("image_path","/home/robot/ws02_tools/src/autopatrol_fishbot/config")
        self.image_path = self.get_parameter("image_path").value
        self.initial_point = self.get_parameter("initial_point").value
        self.target_points = self.get_parameter("target_points").value
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer,self)
        self.client = self.create_client(Speech,"speech_text")
        self.image_latest = None
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image,"camera_sensor/image_raw",self.callback,10)

    def callback(self,msg):
        self.image_latest = msg

    def record_img(self):
        if  self.image_latest:
            transform = self.get_current_pose()
            cv_img = self.bridge.imgmsg_to_cv2(self.image_latest)
            cv2.imwrite(f"{self.image_path}/image_{transform.translation}.png",cv_img)

    def speak(self,text):
        while not self.client.wait_for_service(1.0):
            self.get_logger().info("wait connect for speaker service")
        request = Speech.Request()
        request.text = text
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self,future)
        try:
            if future.result().result:
                self.get_logger().info("speak success")
            else:
                self.get_logger().info("speak failed")
        except Exception as e:
            self.get_logger().info(str(e))

    def get_pose_by_xyyaw(self,x,y,yaw):
        pose = PoseStamped()
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        qtr = tf_transformations.quaternion_from_euler(0.0,0.0,yaw)
        pose.pose.orientation.x = qtr[0]
        pose.pose.orientation.y = qtr[1]
        pose.pose.orientation.z = qtr[2]
        pose.pose.orientation.w = qtr[3]
        return pose
    
    def init_robot_pose(self):
        self.setInitialPose(self.get_pose_by_xyyaw(self.initial_point[0],self.initial_point[1],self.initial_point[2]))
        self.waitUntilNav2Active()

    def get_target_points(self):
        points=[]
        for i in range(int(len(self.target_points)/3)):
            a,b,c=self.target_points[i*3],self.target_points[i*3+1],self.target_points[i*3+2]
            points.append([a,b,c])
            self.get_logger().info(f"get_target_point{i+1}: pose:({a,b}),yaw:{c}")
        return points
    
    def nav2pose(self,targetpose):
            self.goToPose(targetpose)
            while not self.isTaskComplete():
                feedback = self.getFeedback()
                self.get_logger().info(f"estimate remain time:{Duration.from_msg(feedback.estimated_time_remaining).nanoseconds/1e9}s")
            result = self.getResult()
            if result==TaskResult.SUCCEEDED:
                self.get_logger().info("succeed finish task")
            elif result==TaskResult.CANCELED:
                self.get_logger().info("the mission be canceled")
            elif result==TaskResult.FAILED:
                self.get_logger().info("the mission is failed")
            elif result==TaskResult.UNKNOWN:
                self.get_logger().info("the mission is unknowed")

    def get_current_pose(self):
        while rclpy.ok():
            if self.buffer.can_transform("map","base_footprint",Time()):
                tf = self.buffer.lookup_transform("map","base_footprint",Time())
                transform = tf.transform
                euler = tf_transformations.euler_from_quaternion([transform.rotation.x,transform.rotation.y,transform.rotation.z,transform.rotation.w])
                self.get_logger().info(f"pose:{transform.translation},quternion:{transform.rotation},euler:{euler}")
                return transform
            
def main():
    rclpy.init()
    node = Mynode()
    node.speak("位置正在初始化")
    node.init_robot_pose()
    node.speak("位置初始化完成")
    while rclpy.ok():
        count = 1
        points = node.get_target_points()
        for i in points:
            node.speak(f"准备前往第{count}个目标点{i}")
            node.nav2pose(node.get_pose_by_xyyaw(i[0],i[1],i[2]))
            node.speak(f"到达第{count}个目标点{i},开始记录图像")
            node.record_img()
            node.speak("图像记录完成")
            count+=1
    rclpy.shutdown()