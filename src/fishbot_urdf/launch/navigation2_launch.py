from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():
    d1 = DeclareLaunchArgument(name="path",default_value=get_package_share_directory("fishbot_urdf") + "/urdf/xacro/fish_urdf.xacro")
    robot_description = ParameterValue(Command(["xacro ",LaunchConfiguration("path")]))
    robot_state_pub = Node(package="robot_state_publisher",executable="robot_state_publisher",
                            parameters=[{"robot_description":robot_description},{'use_sim_time': True}])
    """ ros2 launch gazebo_ros gazebo.launch.py world:=`ros2 pkg prefix --share fishbot_urdf`/world/custom_room.world verbose:=true  """
    launch_gazebo = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(
            launch_file_path=os.path.join(get_package_share_directory("gazebo_ros"),
                                            "launch",
                                            "gazebo.launch.py"
                                            )
            ),
        launch_arguments={"world":get_package_share_directory("fishbot_urdf") + "/world/custom_room1.world","verbose": "true"}.items()
    )
    spawn_entity_node = Node(package="gazebo_ros",executable="spawn_entity.py",arguments=["-topic","/robot_description","-entity","fishbot"])
    rviz_config_path = DeclareLaunchArgument(name="rviz_config_path",default_value=get_package_share_directory("nav2_bringup")+"/rviz/nav2_default_view.rviz")
    map_yaml_path = DeclareLaunchArgument("map_yaml_path",default_value=get_package_share_directory("fishbot_urdf")+"/maps/room1.yaml")
    nav2_params_yaml_path = DeclareLaunchArgument("nav2_params_yaml_path",default_value=get_package_share_directory("fishbot_urdf")+"/config/nav2_params.yaml")
    launch_nav = IncludeLaunchDescription(
        launch_description_source=PythonLaunchDescriptionSource(launch_file_path=get_package_share_directory("nav2_bringup")+"/launch/bringup_launch.py"),
        launch_arguments={"map":LaunchConfiguration("map_yaml_path"),"use_sim_time":"true","params_file":LaunchConfiguration("nav2_params_yaml_path")}.items())
    rviz = Node(package="rviz2",executable="rviz2",arguments=["-d",LaunchConfiguration("rviz_config_path")],parameters=[{"use_sim_time":True}])
    initiate = Node(package="fishbot_cpp",executable="initialpose_cpp")
    return LaunchDescription([d1,robot_state_pub,launch_gazebo,spawn_entity_node,rviz_config_path,map_yaml_path,nav2_params_yaml_path,launch_nav,rviz,initiate])

