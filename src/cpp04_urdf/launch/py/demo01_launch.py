"from launch import LaunchDescription",
"from launch_ros.actions import Node",
"# 封装终端指令相关类--------------",
"# from launch.actions import ExecuteProcess",
"# from launch.substitutions import FindExecutable",
"# 参数声明与获取-----------------",
"# from launch.actions import DeclareLaunchArgument",
"# from launch.substitutions import LaunchConfiguration",
"# 文件包含相关-------------------",
"# from launch.actions import IncludeLaunchDescription",
"# from launch.launch_description_sources import PythonLaunchDescriptionSource",
"# 分组相关----------------------",
"# from launch_ros.actions import PushRosNamespace",
"# from launch.actions import GroupAction",
"# 事件相关----------------------",
"# from launch.event_handlers import OnProcessStart, OnProcessExit",
"# from launch.actions import ExecuteProcess, RegisterEventHandler,LogInfo",
"# 获取功能包下share目录路径-------",
"# from ament_index_python.packages import get_package_share_directory",
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
def generate_launch_description():
    """ ros2 launch cpp04_urdf demo01_launch.py path:=`ros2 pkg prefix --share cpp04_urdf`/urdf/urdf/urdf_link.urdf """
    d1 = DeclareLaunchArgument(name="path",default_value=get_package_share_directory("cpp04_urdf") + "/urdf/urdf/demo01_urdf.urdf")
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("path")]))
    robot_state_pub = Node(package="robot_state_publisher",executable="robot_state_publisher",
                           parameters=[{"robot_description":robot_description}])
    joint_state_pub = Node(package="joint_state_publisher",executable="joint_state_publisher")
    rviz2 = Node(package="rviz2",executable="rviz2",arguments=["-d",get_package_share_directory("cpp04_urdf") + "/rviz/urdf.rviz"])
    return LaunchDescription([d1,robot_state_pub,joint_state_pub,rviz2])