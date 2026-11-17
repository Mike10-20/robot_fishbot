#include "fishbot_plugin/nav2_custom_controller.hpp"
#include "nav2_core/exceptions.hpp"
#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <cmath>

namespace nav2_custom_controller
{

    void Customcontroller::configure(
        const rclcpp_lifecycle::LifecycleNode::WeakPtr &parent,
        std::string name, std::shared_ptr<tf2_ros::Buffer> buffer,
        std::shared_ptr<nav2_costmap_2d::Costmap2DROS> costmap)
    {
        node_ = parent.lock();
        name_ = name;
        buffer_ = buffer;
        costmap_ = costmap->getCostmap();
        global_frame_id_ = costmap->getGlobalFrameID();
        robot_frame_id = costmap->getBaseFrameID();
        nav2_util::declare_parameter_if_not_declared(node_, name_ + ".max_angle_velocity", rclcpp::ParameterValue(1.0));
        nav2_util::declare_parameter_if_not_declared(node_, name_ + ".max_line_velocity", rclcpp::ParameterValue(0.1));
        node_->get_parameter(name_ + ".max_angle_velocity", max_angle);
        node_->get_parameter(name_ + ".max_line_velocity", max_line);
    }

    void Customcontroller::cleanup()
    {
        RCLCPP_INFO(node_->get_logger(), "正在clean %s controller plugin", name_.c_str());
    }

    void Customcontroller::activate()
    {
        RCLCPP_INFO(node_->get_logger(), "正在activate %s controller plugin", name_.c_str());
    }

    void Customcontroller::deactivate()
    {
        RCLCPP_INFO(node_->get_logger(), "正在deactivate %s controller plugin", name_.c_str());
    }

    void Customcontroller::setPlan(const nav_msgs::msg::Path &path)
    {
        global_path_ = path;
    }

    geometry_msgs::msg::TwistStamped Customcontroller::computeVelocityCommands(
        const geometry_msgs::msg::PoseStamped &pose,
        const geometry_msgs::msg::Twist &velocity,
        nav2_core::GoalChecker *goal_checker)
    {
        (void)goal_checker;
        (void)velocity;
        if (global_path_.poses.empty())
        {
            throw nav2_core::PlannerException("receive length of global_path_.poses is 0");
        }
        // geometry_msgs::msg::PoseStamped pose1;
        // nav2_util::transformPoseInTargetFrame(pose,pose1,*buffer_,global_frame_id_,0.1);
        geometry_msgs::msg::PoseStamped nearnest = get_nearnest_point(pose);
        double angle = get_angle_diff(pose, nearnest);
        geometry_msgs::msg::TwistStamped twist;
        twist.header.stamp = node_->now();
        twist.header.frame_id = robot_frame_id;
        if (fabs(angle) > M_PI / 10.0)
        {
            twist.twist.angular.z = fabs(angle) / angle * max_angle;
            twist.twist.linear.x = 0.0;
        }
        else
        {
            twist.twist.linear.x = max_line;
            twist.twist.angular.z = 0.0;
        }
        RCLCPP_INFO(node_->get_logger(), "controller send velocity: line(%.2f),angle(%.2f)", twist.twist.linear.x, twist.twist.angular.z);
        return twist;
    }

    void Customcontroller::setSpeedLimit(const double &speed_limit, const bool &percentage)
    {
        (void)speed_limit;
        (void)percentage;
    }

    double Customcontroller::get_angle_diff(geometry_msgs::msg::PoseStamped start,
                                            geometry_msgs::msg::PoseStamped end)
    {
        double x = end.pose.position.x - start.pose.position.x;
        double y = end.pose.position.y - start.pose.position.y;
        double re = atan2(y, x) - tf2::getYaw(start.pose.orientation);
        cout<<re<<endl;
        if (re < -M_PI)
        {
            re += 2.0 * M_PI;
        }
        else if (re > M_PI)
        {
            re -= 2.0 * M_PI;
        }
        return re;
    }

    geometry_msgs::msg::PoseStamped Customcontroller::get_nearnest_point(
        geometry_msgs::msg::PoseStamped current_pose)
    {
        int index = 0;
        double min_distance = nav2_util::geometry_utils::euclidean_distance(current_pose, global_path_.poses.at(0));
        for (unsigned int i = 0; i < global_path_.poses.size(); i++)
        {
            double dis = nav2_util::geometry_utils::euclidean_distance(current_pose, global_path_.poses[i]);
            if (dis < min_distance)
            {
                index = i;
                min_distance = dis;
            }
        }
        global_path_.poses.erase(global_path_.poses.begin(), global_path_.poses.begin() + index);
        if (global_path_.poses.empty())
        {
            return current_pose;
        }
        else if (global_path_.poses.size() > 1)
        {
            return global_path_.poses[1];
        }
        else
        {
            return global_path_.poses[0];
        }
    }

}
#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(nav2_custom_controller::Customcontroller, nav2_core::Controller)