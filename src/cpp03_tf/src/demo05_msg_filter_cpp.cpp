#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"
#include "tf2_ros/transform_listener.hpp"
#include "tf2_ros/buffer.hpp"
#include "tf2_ros/create_timer_ros.hpp"
#include "tf2_ros/message_filter.hpp"
#include "tf2_geometry_msgs/tf2_geometry_msgs.hpp"
#include "message_filters/subscriber.hpp"
using geometry_msgs::msg::PointStamped;
using namespace std::chrono_literals;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("msg_filters__node")
    {
        buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
        timer_ = std::make_shared<tf2_ros::CreateTimerROS>(
            this->get_node_base_interface(),
            this->get_node_timers_interface()
        );
        listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_,this);
        buffer_->setCreateTimerInterface(timer_);
        sub.subscribe(this,"point");
        filter_ = std::make_shared<tf2_ros::MessageFilter<PointStamped>>(sub,*buffer_,"base_link",10,
            this->get_node_logging_interface(),
        this->get_node_clock_interface(),
            1s);
        filter_->registerCallback(&Mynode::callback,this);
    }
private:
    void callback(const PointStamped &msg)
    {
        auto p = buffer_->transform(msg,"base_link");
        RCLCPP_INFO(this->get_logger(),"frame-id: %s,(%.2f,%.2f,%.2f)",p.header.frame_id.c_str(),p.point.x,p.point.y,p.point.z);
    }
    std::unique_ptr<tf2_ros::Buffer> buffer_;
    std::shared_ptr<tf2_ros::CreateTimerROS> timer_;
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    message_filters::Subscriber<PointStamped> sub;
    std::shared_ptr<tf2_ros::MessageFilter<PointStamped>> filter_;

};
int main(int argc,char **argv)
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Mynode>());
    rclcpp::shutdown();

}