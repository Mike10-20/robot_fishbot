#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"
using geometry_msgs::msg::PoseWithCovarianceStamped;
using namespace std::chrono_literals;

class Mynode:public rclcpp::Node
{
public:
  Mynode():Node("initial_pose_cpp_node")
  {
    pub_ = this->create_publisher<PoseWithCovarianceStamped>("/initialpose",10);
    rclcpp::Rate rate(1.0);
    rate.sleep();
    this->send();
  }
private:
  rclcpp::Publisher<PoseWithCovarianceStamped>::SharedPtr pub_;
  rclcpp::TimerBase::SharedPtr timer_;
  void send()
  {
    PoseWithCovarianceStamped pose;
    pose.header.frame_id = "map";
    pose.header.stamp = this->now();
    pose.pose.pose.position.x = 0.0;
    pose.pose.pose.position.y = 0.0;
    pose.pose.pose.position.z = 0.0;
    pub_->publish(pose);
  }
};
int main(int argc,char **argv)
{
  rclcpp::init(argc,argv);
  auto node = std::make_shared<Mynode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
}