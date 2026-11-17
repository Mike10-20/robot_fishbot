#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "turtlesim/msg/pose.hpp"
#include "tf2/LinearMath/Quaternion.hpp"
using tf2::Quaternion;
using geometry_msgs::msg::TransformStamped;
using turtlesim::msg::Pose;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("dynamic_tf_broadcaster_cpp_node")
    {
        sub_ = this->create_subscription<Pose>("/turtle1/pose",10,
        std::bind(&Mynode::callback,this,std::placeholders::_1));
        broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
    }
private:
    rclcpp::Subscription<Pose>::SharedPtr sub_;
    std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
    void callback(const Pose &msg)
    {
        TransformStamped ts;
        ts.header.frame_id = "world";
        ts.header.stamp = this->now();
        ts.child_frame_id = "turtle1";
        ts.transform.translation.x = msg.x;
        ts.transform.translation.y = msg.y;
        ts.transform.translation.z = 0.0;
        Quaternion qt;
        qt.setRPY(0.0,0.0,msg.theta);
        ts.transform.rotation.x = qt.x();
        ts.transform.rotation.y = qt.y();
        ts.transform.rotation.z = qt.z();
        ts.transform.rotation.w = qt.w();
        broadcaster_->sendTransform(ts);
    }

};
int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Mynode>());
    rclcpp::shutdown();
}
