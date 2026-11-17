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
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import ExecuteProcess
def generate_launch_description():
    t1 = Node(package="turtlesim",executable="turtlesim_node",name="t1",parameters=[{"background_r":255}],
              namespace="t3",exec_name="tortoise",respawn = True  )
    t3 = Node(package="turtlesim",executable="turtlesim_node",ros_arguments=["--remap","__ns:=/t1"])
    t4 = Node(package="turtlesim",remappings=[("/t1/turtle1/cmd_vel","/cmd_vel")],executable="turtlesim_node",ros_arguments=["--remap","__ns:=/t1"],arguments=["12"],
              parameters=[os.path.join(get_package_share_directory("cpp01_launch"),"config","turtlesim.yaml")])
    t2 = Node(package="turtlesim",remappings=[("/t1/turtle1/cmd_vel","/cmd_vel")],executable="turtlesim_node",ros_arguments=["--remap","__ns:=/t1"],parameters=["/home/robot/ws02_tools/install/cpp01_launch/share/cpp01_launch/config/turtlesim.yaml"])
    echo1 = ExecuteProcess(
        cmd=["ros2 topic echo /t1/turtle1/pose"],
        output = "both",
        shell = True)
    bkg_r = DeclareLaunchArgument(name="backg_r",default_value="255")
    bkg_g = DeclareLaunchArgument(name="backg_g",default_value="255")
    bkg_b = DeclareLaunchArgument(name="backg_b",default_value="255")
    t5 = Node(package="turtlesim",executable="turtlesim_node",parameters=[{"background_r": LaunchConfiguration("backg_r"),"background_g": LaunchConfiguration("backg_g"),"background_b": LaunchConfiguration("backg_b")}])
    return LaunchDescription([bkg_r,bkg_g,bkg_b,t5])