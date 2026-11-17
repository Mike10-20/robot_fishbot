#ifndef PLANNER
#define PLANNER
#include "geometry_msgs/msg/pose_stamped.hpp"
#include "geometry_msgs/msg/point.hpp"
#include "rclcpp/rclcpp.hpp"
#include "nav2_core/global_planner.hpp"
#include "nav2_costmap_2d/costmap_2d_ros.hpp"
#include "nav2_util/lifecycle_node.hpp"
#include "nav2_util/robot_utils.hpp"
#include "nav2_util/node_utils.hpp"
#include "nav_msgs/msg/path.hpp"
#include <memory>
#include <string>

using namespace std;
namespace nav2_custom_plannner
{
    class CustomPlanner : public nav2_core::GlobalPlanner
    {
    public:
        CustomPlanner() = default;
        ~CustomPlanner() = default;
        void configure(
            const rclcpp_lifecycle::LifecycleNode::WeakPtr &parent,
            std::string name, std::shared_ptr<tf2_ros::Buffer> tf,
            std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros);

        void cleanup();

        void activate();

        void deactivate();

        nav_msgs::msg::Path createPlan(
            const geometry_msgs::msg::PoseStamped &start,
            const geometry_msgs::msg::PoseStamped &goal);
    private:
        std::shared_ptr<tf2_ros::Buffer> buffer_;
        nav2_util::LifecycleNode::SharedPtr node_;
        nav2_costmap_2d::Costmap2D *costmap_;
        std::string global_frame_,name_;
        double interpolation_resolution_;
    };
}

#endif