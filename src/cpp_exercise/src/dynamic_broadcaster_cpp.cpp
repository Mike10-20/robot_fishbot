#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_broadcaster.hpp"
#include "tf2/LinearMath/Quaternion.hpp"
#include "turtlesim/msg/pose.hpp"
using namespace std;
#include "geometry_msgs/msg/transform_stamped.hpp"
using turtlesim::msg::Pose;
using geometry_msgs::msg::TransformStamped;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("dynamic_broadcaster_cpp_node")
    {
        this->declare_parameter("frame-id","world");
        this->declare_parameter("child-frame-id","turtle1");
        father = this->get_parameter("frame-id").as_string();
        child = this->get_parameter("child-frame-id").as_string();
        broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        sub_ = this->create_subscription<Pose>("/"+child+"/pose",10,std::bind(&Mynode::callback,this,std::placeholders::_1));
    } 
private:
    string father,child;
    void callback(const Pose &msg)
    {

        TransformStamped tf;
        tf.header.stamp = this->now();
        tf.header.frame_id = father;
        tf.child_frame_id = child;
        tf.transform.translation.x = msg.x;
        tf.transform.translation.y = msg.y;
        tf.transform.translation.z = 0;
        tf2::Quaternion qt;
        qt.setRPY(0.0,0.0,msg.theta);
        tf.transform.rotation.x = qt.x();
        tf.transform.rotation.y = qt.y();
        tf.transform.rotation.z = qt.z();
        tf.transform.rotation.w = qt.w();
        broadcaster_->sendTransform(tf);
    }
    std::shared_ptr<tf2_ros::TransformBroadcaster> broadcaster_;
    rclcpp::Subscription<Pose>::SharedPtr sub_;

};
int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Mynode>());
    rclcpp::shutdown();
}