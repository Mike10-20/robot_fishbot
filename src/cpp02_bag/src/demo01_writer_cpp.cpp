#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "rosbag2_cpp/writer.hpp"
using geometry_msgs::msg::Twist;
class Mynode:public rclcpp::Node
{
public:
  Mynode():Node("rosbag2_cpp_node")
  {
    writer_ = std::make_unique<rosbag2_cpp::Writer>();
    writer_->open("my_bag");
    sub_ = this->create_subscription<Twist>("/turtle1/cmd_vel",10,std::bind(&Mynode::callback,this,std::placeholders::_1));
  }
private:
  void callback(std::shared_ptr<const rclcpp::SerializedMessage> message)
  {
    RCLCPP_INFO(this->get_logger(),"dumping----");
    writer_->write(message,"turtle1/cmd_vel","geometry_msgs/msg/Twist",this->now());
  }
  std::unique_ptr<rosbag2_cpp::Writer> writer_;
  rclcpp::Subscription<Twist>::SharedPtr sub_;
};
int main(int argc,char** argv)
{
  rclcpp::init(argc,argv);
  rclcpp::spin(std::make_shared<Mynode>());
  rclcpp::shutdown();
}