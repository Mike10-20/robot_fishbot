from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

from launch.event_handlers import OnProcessStart, OnProcessExit
from launch.actions import ExecuteProcess, RegisterEventHandler,LogInfo
def generate_launch_description():
   
    t1 = Node(package="turtlesim",executable="turtlesim_node")
    p1 = ExecuteProcess(
        cmd=["ros2 service call /spawn turtlesim/srv/Spawn \"{'x': 9,'y': 9}\""],
        output = "both",
        shell = True
    )
    event1 = RegisterEventHandler(
        event_handler=OnProcessStart(
            target_action=t1,
            on_start=p1
        ))
    event2 = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=t1,
            on_exit=LogInfo(msg="client exit*****")
        )
    )
    
    return LaunchDescription([t1,event1,event2])