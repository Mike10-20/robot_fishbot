#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/transform_listener.hpp"
#include "tf2_ros/buffer.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2/utils.h"
using tf2::Quaternion;
using namespace std::chrono_literals;
class Mynode : public rclcpp::Node
{
public:
    Mynode() : Node("dynamic_tf_listener_cpp_node")
    {
        buffer_ = std::make_unique<tf2_ros::Buffer>(this->get_clock());
        listener_ = std::make_shared<tf2_ros::TransformListener>(*buffer_, this);
        timer_ = this->create_wall_timer(1s, std::bind(&Mynode::callback, this));
    }

private:
    std::shared_ptr<tf2_ros::TransformListener> listener_;
    std::unique_ptr<tf2_ros::Buffer> buffer_;
    rclcpp::TimerBase::SharedPtr timer_;
    void callback()
    {
        // try
        // {
        //     auto tf = buffer_->lookupTransform("map","base_footprint",tf2::TimePointZero);
        //     Quaternion qtr(tf.transform.rotation.x,tf.transform.rotation.y,tf.transform.rotation.z,tf.transform.rotation.w);
        //     RCLCPP_INFO(this->get_logger(),"(%.2f,%.2f),%.2f",tf.transform.translation.x,tf.transform.translation.y,qtr.getAngle());

        // }
        // catch (tf2::LookupException &e)
        // {
        //     RCLCPP_INFO(this->get_logger(),e.what());
        // }
        if (buffer_->canTransform("map", "base_footprint", tf2::TimePointZero))
        {
            auto tf = buffer_->lookupTransform("map","base_footprint",tf2::TimePointZero);
            Quaternion qtr(tf.transform.rotation.x, tf.transform.rotation.y, tf.transform.rotation.z, tf.transform.rotation.w);
            double yaw,pitch,roll;
            tf2::getEulerYPR(qtr,yaw,pitch,roll);
            RCLCPP_INFO(this->get_logger(), "(%.2f,%.2f),%.2f", tf.transform.translation.x, tf.transform.translation.y, yaw);
        }
        
    }
};
int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<Mynode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
}