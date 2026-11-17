from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
def generate_launch_description():

    p1 = DeclareLaunchArgument(name="child2",default_value="t2")
    p2 = DeclareLaunchArgument(name="child3",default_value="t3")
    p3 = DeclareLaunchArgument(name="child4",default_value="t4")
    t1 = Node(package="turtlesim",executable="turtlesim_node")
    child2 = Node(package="cpp_exercise",executable="spawn_cpp",name="spawn_t2",parameters=[{"x":1.3,"y":1.3,"theta":0.0,"name":LaunchConfiguration("child2")}])
    child3 = Node(package="cpp_exercise",executable="spawn_cpp",name="spawn_t3",parameters=[{"x":1.0,"y":1.0,"theta":0.0,"name":LaunchConfiguration("child3")}])
    child4 = Node(package="cpp_exercise",executable="spawn_cpp",name="spawn_t4",parameters=[{"x":2.0,"y":2.0,"theta":0.0,"name":LaunchConfiguration("child4")}])
    
    t1_bc = Node(package="cpp_exercise",executable="dynamic_broadcaster_cpp",name="broadcaster_turtle1",parameters=[{"frame-id":"world","child-frame-id":"turtle1"}])
    t2_bc = Node(package="cpp_exercise",executable="dynamic_broadcaster_cpp",name="broadcaster_t2",parameters=[{"frame-id":"world","child-frame-id":LaunchConfiguration("child2")}])
    t3_bc = Node(package="cpp_exercise",executable="dynamic_broadcaster_cpp",name="broadcaster_t3",parameters=[{"frame-id":"world","child-frame-id":LaunchConfiguration("child3")}])
    t4_bc = Node(package="cpp_exercise",executable="dynamic_broadcaster_cpp",name="broadcaster_t4",parameters=[{"frame-id":"world","child-frame-id":LaunchConfiguration("child4")}])
    
    goal2 = Node(package="tf2_ros",executable="static_transform_publisher",arguments=["--frame-id","turtle1","--child-frame-id","goal2","--x","-3"])
    goal3 = Node(package="tf2_ros",executable="static_transform_publisher",arguments=["--frame-id","turtle1","--child-frame-id","goal3","--x","-1.5","--y","1.5"])
    goal4 = Node(package="tf2_ros",executable="static_transform_publisher",arguments=["--frame-id","turtle1","--child-frame-id","goal4","--x","-1.5","--y","-1.5"])


    t1_goal2 = Node(package="cpp_exercise",executable="listener_cpp",name="t1_goal2",parameters=[{"father":LaunchConfiguration("child2"),"child":"goal2"}])
    t1_goal3 = Node(package="cpp_exercise",executable="listener_cpp",name="t1_goal3",parameters=[{"father":LaunchConfiguration("child3"),"child":"goal3"}])
    t1_goal4 = Node(package="cpp_exercise",executable="listener_cpp",name="t1_goal4",parameters=[{"father":LaunchConfiguration("child4"),"child":"goal4"}])
   

    return LaunchDescription([p1,p2,p3,t1,child2,child3,child4,t1_bc,t2_bc,t3_bc,t4_bc,goal2,goal3,goal4,t1_goal2,t1_goal3,t1_goal4])