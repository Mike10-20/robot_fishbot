from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
def generate_launch_description():
    """ ros2 launch cpp04_urdf demo01_launch.py path:=`ros2 pkg prefix --share cpp04_urdf`/urdf/urdf/urdf_link.urdf """
    d1 = DeclareLaunchArgument(name="path",default_value=get_package_share_directory("fishbot_urdf") + "/urdf/xacro/fish_urdf.xacro")
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("path")]))
    robot_state_pub = Node(package="robot_state_publisher",executable="robot_state_publisher",
                           parameters=[{"robot_description":robot_description}])
    joint_state_pub = Node(package="joint_state_publisher",executable="joint_state_publisher")
    rviz2 = Node(package="rviz2",executable="rviz2",arguments=["-d",get_package_share_directory("fishbot_urdf")+"/config/fishbot.rviz"])
    return LaunchDescription([d1,robot_state_pub,joint_state_pub,rviz2])

