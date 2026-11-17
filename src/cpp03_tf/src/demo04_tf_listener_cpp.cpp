#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_listener.hpp"
#include "tf2_ros/buffer.hpp"
using namespace std::chrono_literals;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("tf_listener_cpp_node")
    {
        buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
        listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_,this);
        timer_ = this->create_wall_timer(1s,std::bind(&Mynode::callback,this));
    }   
private:
    void callback()
    {
         /*  geometry_msgs::msg::TransformStamped
  lookupTransform(
    const std::string & target_frame, const std::string & source_frame,
    const TimePoint & time) const override; */
        try
        {
            auto tf = buffer_->lookupTransform("camera","laser",tf2::TimePointZero);
            RCLCPP_INFO(this->get_logger(),"frame-id: %s,child-frame-id: %s,(%.2f,%.2f,%.2f)",
            tf.header.frame_id.c_str(),
        tf.child_frame_id.c_str(),tf.transform.translation.x,tf.transform.translation.y,tf.transform.translation.z);
            

        }
        catch(const tf2::LookupException & e)
        {
            RCLCPP_INFO(this->get_logger(),"error %s",e.what());
        }
        
    }
    std::unique_ptr<tf2_ros::Buffer> buffer_;
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    rclcpp::TimerBase::SharedPtr timer_;
};
int main(int argc,char **argv)
{
    rclcpp::init(argc,argv);
    rclcpp::spin(std::make_shared<Mynode>());
    rclcpp::shutdown();
}