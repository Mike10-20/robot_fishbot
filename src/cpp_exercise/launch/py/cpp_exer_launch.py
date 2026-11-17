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
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
def generate_launch_description():

    p1 = DeclareLaunchArgument(name="child",default_value="t2")
    t1 = Node(package="turtlesim",executable="turtlesim_node")
    t2 = Node(package="cpp_exercise",executable="spawn_cpp",name="spawn",parameters=[{"x":5.0,"y":5.0,"theta":0.0,"name":LaunchConfiguration("child")}])
    t3 = Node(package="cpp_exercise",executable="dynamic_broadcaster_cpp",name = "broadcaster_turtle1",parameters=[{"frame-id":"world","child-frame-id":"turtle1"}])
    t4 = Node(package="cpp_exercise",executable="dynamic_broadcaster_cpp",parameters=[{"frame-id":"world","name":LaunchConfiguration("child"),"father":"t2_frame"}])
    t5 = Node(package="cpp_exercise",executable="listener_cpp",parameters=[{"father":LaunchConfiguration("child"),"child":"turtle1"}])
    return LaunchDescription([p1,t1,t2,t3,t4,t5])