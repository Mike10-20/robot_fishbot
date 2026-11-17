#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"
using geometry_msgs::msg::PointStamped;
using namespace std::chrono_literals;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("tf_point_broadcaster_cpp_node")
    {
        x = 0.0;
        pub_ = this->create_publisher<PointStamped>("/point",10);
        timer_ = this->create_wall_timer(1s,std::bind(&Mynode::callback,this));
    }
private:
    void callback()
    {
        PointStamped p;
        p.header.frame_id = "laser";
        p.header.stamp = this->now();
        p.point.x = x;
        p.point.y = 0;
        p.point.z = -1;
        x += 0.05;
        pub_->publish(p);
    }
    double_t x;
    rclcpp::Publisher<PointStamped>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};
int main(int argc,char ** argv)
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Mynode>());
    rclcpp::shutdown();
}