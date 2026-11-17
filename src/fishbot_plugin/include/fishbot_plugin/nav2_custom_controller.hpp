#ifndef CONTROLLER
#define CONTROLLER
#include "nav2_core/global_planner.hpp"
#include "nav2_core/controller.hpp"
#include "nav_msgs/msg/path.hpp"
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "nav2_util/node_utils.hpp"
#include "nav2_util/robot_utils.hpp"
#include "nav2_util/geometry_utils.hpp"
#include "nav2_util/lifecycle_node.hpp"
#include "nav2_costmap_2d/costmap_2d_ros.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std;
namespace nav2_custom_controller
{
    class Customcontroller : public nav2_core::Controller
    {
    public:
        void configure(
            const rclcpp_lifecycle::LifecycleNode::WeakPtr & parent,
            std::string name, std::shared_ptr<tf2_ros::Buffer> buffer,
            std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap);

        void cleanup();

        void activate();

        void deactivate();

        void setPlan(const nav_msgs::msg::Path &path);

        double get_angle_diff(geometry_msgs::msg::PoseStamped start,
            geometry_msgs::msg::PoseStamped end);

        geometry_msgs::msg::TwistStamped computeVelocityCommands(
            const geometry_msgs::msg::PoseStamped &pose,
            const geometry_msgs::msg::Twist &velocity,
            nav2_core::GoalChecker *goal_checker);

        void setSpeedLimit(const double &speed_limit, const bool &percentage);

        geometry_msgs::msg::PoseStamped get_nearnest_point(
            geometry_msgs::msg::PoseStamped current_pose);
    protected:
        std::shared_ptr<tf2_ros::Buffer> buffer_;
        string name_,global_frame_id_,robot_frame_id;
        nav_msgs::msg::Path global_path_;
        nav2_util::LifecycleNode::SharedPtr node_;
        nav2_costmap_2d::Costmap2D * costmap_;
        double max_angle,max_line;
    };
}
#endif