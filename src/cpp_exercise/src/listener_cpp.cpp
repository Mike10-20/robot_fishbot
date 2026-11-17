#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/buffer.hpp"
#include "tf2_ros/transform_listener.hpp"
#include "geometry_msgs/msg/twist.hpp"
using geometry_msgs::msg::Twist;
using namespace std;
using namespace std::chrono_literals;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("listener_cpp_node")
    {
        this->declare_parameter("child","turtle1");
        this->declare_parameter("father","t2");
        father = this->get_parameter("father").as_string();
        child = this->get_parameter("child").as_string();
        buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
        listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_,this);
        pub_ = this->create_publisher<Twist>("/"+father+"/cmd_vel",10);
        timer_ = this->create_wall_timer(1s,std::bind(&Mynode::callback,this));

    }
private:
    void callback()
    {
        try
        {
            auto tf = buffer_->lookupTransform(father,child,tf2::TimePointZero);
            float x = tf.transform.translation.x;
            float y = tf.transform.translation.y;
            float x_vel = 0.5*sqrt(pow(x,2)+pow(y,2));
            float yaw_vel = 1*atan2(y,x);
            Twist tw;
            tw.linear.x = x_vel;
            tw.angular.z = yaw_vel;
            pub_->publish(tw);
        }
        catch (tf2::LookupException & e)
        {
            RCLCPP_INFO(this->get_logger(),"%s",e.what());
        }
    }
    std::unique_ptr<tf2_ros::Buffer> buffer_;
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::Publisher<Twist>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    string child,father,name;
};
int main(int argc,char**argv)
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Mynode>());
    rclcpp::shutdown();
}