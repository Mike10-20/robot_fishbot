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
    """ ros2 launch cpp04_urdf demo01_launch.py path:=`ros2 pkg prefix --share cpp04_urdf`/urdf/urdf/urdf_link.urdf """
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
    rviz2 = Node(package="rviz2",executable="rviz2",arguments=["-d",get_package_share_directory("fishbot_urdf")+"/config/fishbot.rviz"],parameters=[{'use_sim_time': True}])
    # joint_state_pub = Node(package="joint_state_publisher",executable="joint_state_publisher")
    launch_slam = IncludeLaunchDescription(
            launch_description_source=PythonLaunchDescriptionSource(
                launch_file_path=os.path.join(get_package_share_directory("slam_toolbox"),
                                              "launch",
                                              "online_async_launch.py"
                                              )
                ),
            launch_arguments={"use_sim_time":"true"}.items()
        )
    
    return LaunchDescription([d1,robot_state_pub,launch_gazebo,spawn_entity_node,rviz2,launch_slam])