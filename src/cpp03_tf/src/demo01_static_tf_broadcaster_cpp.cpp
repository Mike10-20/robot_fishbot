#include "rclcpp/rclcpp.hpp"
#include "tf2_ros/static_transform_broadcaster.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2/LinearMath/Quaternion.hpp"
using geometry_msgs::msg::TransformStamped;
class Mynode:public rclcpp::Node
{
public:
  Mynode(char *argv[]):Node("static_tf_broadcaster_node")
  {
    broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);
    send_tf(argv);
  }
private:
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> broadcaster_;
  void send_tf(char *argv[]);
};
void Mynode::send_tf(char *argv[])
{
  TransformStamped tf;
  tf.header.stamp = this->now();
  tf.header.frame_id = argv[7];
  tf.child_frame_id = argv[8];
  tf2::Quaternion qt;
  qt.setRPY(atof(argv[4]),atof(argv[5]),atof(argv[6]));
  tf.transform.translation.x = atof(argv[1]);
  tf.transform.translation.y = atof(argv[2]);
  tf.transform.translation.z = atof(argv[3]);
  tf.transform.rotation.x = qt.x();
  tf.transform.rotation.y = qt.y();
  tf.transform.rotation.z = qt.z();
  tf.transform.rotation.w = qt.w();

  broadcaster_->sendTransform(tf);
}
int main(int argc,char*argv[])
{
  if (argc!=9)
  {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"),"please input 8 parameter");
    return 0;
  }
  rclcpp::init(argc,argv);
  rclcpp::spin(std::make_shared<Mynode>(argv));
  rclcpp::shutdown();
}