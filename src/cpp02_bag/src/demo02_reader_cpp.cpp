#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "rosbag2_cpp/reader.hpp"
using geometry_msgs::msg::Twist;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("rosbag2_reader_cpp_node")
    {
        reader_ = std::make_unique<rosbag2_cpp::Reader>();
        reader_->open("my_bag");
        while (reader_->has_next())
        {
            count++;
            Twist mes = reader_->read_next<Twist>();
            RCLCPP_INFO(this->get_logger(),"velocity:%.2f,angle_vel:%.2f,%ld",mes.linear.x,mes.angular.z,count);
        }
        reader_->close();
    }
private:
    std::unique_ptr<rosbag2_cpp::Reader> reader_;
    size_t count=0;
};
int main(int argc,char** argv)
{
  rclcpp::init(argc,argv);
  std::make_shared<Mynode>();
  rclcpp::shutdown();
}