#include "fishbot_plugin/nav2_custom_planner.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "nav2_core/exceptions.hpp"
namespace nav2_custom_plannner
{
    void CustomPlanner::configure(
        const rclcpp_lifecycle::LifecycleNode::WeakPtr &parent,
        std::string name, std::shared_ptr<tf2_ros::Buffer> tf,
        std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap_ros)
    {
        buffer_ = tf;
        name_ = name;
        node_ = parent.lock();
        this->costmap_ = costmap_ros->getCostmap();
        global_frame_ = costmap_ros->getGlobalFrameID();
        nav2_util::declare_parameter_if_not_declared(node_, name_ + ".interpolation_resolution", rclcpp::ParameterValue(0.1));
        node_->get_parameter(name_ + ".interpolation_resolution", interpolation_resolution_);
    }

    void CustomPlanner::cleanup()
    {
        RCLCPP_INFO(node_->get_logger(), "正在清理类型为CustomPlanner的插件 %s", name_.c_str());
    }

    void CustomPlanner::activate()
    {
        RCLCPP_INFO(node_->get_logger(), "正激活类型为CustomPlanner的插件 %s", name_.c_str());
    }

    void CustomPlanner::deactivate()
    {
        RCLCPP_INFO(node_->get_logger(), "正停用类型为CustomPlanner的插件 %s", name_.c_str());
    }

    nav_msgs::msg::Path CustomPlanner::createPlan(
        const geometry_msgs::msg::PoseStamped &start,
        const geometry_msgs::msg::PoseStamped &goal)
    {
        nav_msgs::msg::Path goal_path;
        goal_path.poses.clear();
        goal_path.header.stamp = node_->now();
        goal_path.header.frame_id = global_frame_;
        if (start.header.frame_id != global_frame_)
        {
            RCLCPP_ERROR(node_->get_logger(), "start的frame_id与global_fram_id不一致");
            return goal_path;
        }
        if (goal.header.frame_id != global_frame_)
        {
            RCLCPP_ERROR(node_->get_logger(), "goal的frame_id与global_fram_id不一致");
            return goal_path;
        }
        int a = hypot(goal.pose.position.x - start.pose.position.x, goal.pose.position.y - start.pose.position.y) / interpolation_resolution_;
        double x_increment = (goal.pose.position.x - start.pose.position.x) / a;
        double y_increment = (goal.pose.position.y - start.pose.position.y) / a;
        for (int i = 0; i < a; i++)
        {
            geometry_msgs::msg::PoseStamped pose;
            pose.header.stamp = node_->now();
            pose.header.frame_id = global_frame_;
            pose.pose.position.x = start.pose.position.x + i * x_increment;
            pose.pose.position.y = start.pose.position.y + i * y_increment;
            goal_path.poses.push_back(pose);
        }
        for (geometry_msgs::msg::PoseStamped pose : goal_path.poses)
        {
            unsigned int mx, my;
            if (costmap_->worldToMap(pose.pose.position.x, pose.pose.position.y, mx, my))
            {
                unsigned char cost = costmap_->getCost(mx, my);
                if (cost == nav2_costmap_2d::LETHAL_OBSTACLE)
                {
                    RCLCPP_WARN(node_->get_logger(), "检测到obstruct at (%f,%f)", pose.pose.position.x, pose.pose.position.y);
                    throw nav2_core::PlannerException("无法创建目标规划to(" + to_string(pose.pose.position.x) + "," + to_string(pose.pose.position.y) + ")");
                }
            }
        }
        geometry_msgs::msg::PoseStamped pose=goal;
        pose.header.stamp = node_->now();
        pose.header.frame_id = global_frame_;
        goal_path.poses.push_back(pose);
        return goal_path;
    }
}
#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(nav2_custom_plannner::CustomPlanner, nav2_core::GlobalPlanner)