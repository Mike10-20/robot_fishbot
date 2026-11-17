from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
def generate_launch_description():
    nav_path = os.path.join(get_package_share_directory("fishbot_urdf"),"launch","navigation2_launch.py")
    include = IncludeLaunchDescription(launch_description_source=PythonLaunchDescriptionSource(nav_path))
    param_path = os.path.join(get_package_share_directory("autopatrol_fishbot"),"config","patrol_param.yaml")
    t1 = Node(package="autopatrol_fishbot",executable="patrol_node",parameters=[param_path])
    t2 = Node(package="autopatrol_fishbot",executable="speaker")
    return LaunchDescription([include,t1,t2])