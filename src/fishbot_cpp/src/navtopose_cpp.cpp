#include "rclcpp/rclcpp.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"
#include "rclcpp_action/create_client.hpp"
#include "tf2/LinearMath/Quaternion.hpp"
using nav2_msgs::action::NavigateToPose;
using namespace std::chrono_literals;
class Mynode:public rclcpp::Node
{
public:
    Mynode():Node("navtopose_cpp_node")
    {
        client_ = rclcpp_action::create_client<NavigateToPose>(this,"/navigate_to_pose");
        
    }
    void sendgoal()
    {
        if (!client_->wait_for_action_server(10s))
        {
            RCLCPP_INFO(this->get_logger(),"can't connect for server");
            return;
        }
        RCLCPP_INFO(this->get_logger(),"succeed connect for server");

        NavigateToPose::Goal goal;
        goal.pose.header.stamp = this->now();
        goal.pose.header.frame_id = "map";
        goal.pose.pose.position.x = 0.5;
        goal.pose.pose.position.y = 0.5;
        goal.pose.pose.position.z = 0.0;
        tf2::Quaternion qt;
        qt.setEuler(0.0,0.0,1.57);
        goal.pose.pose.orientation.x = qt.x();
        goal.pose.pose.orientation.y = qt.y();
        goal.pose.pose.orientation.z = qt.z();
        goal.pose.pose.orientation.w = qt.w();
        /*   using GoalResponseCallback = std::function<void (typename GoalHandle::SharedPtr)>;
          using FeedbackCallback =
    std::function<void (
        typename ClientGoalHandle<ActionT>::SharedPtr,
        const std::shared_ptr<const Feedback>)>;
  using ResultCallback = std::function<void (const WrappedResult & result)>; */
        rclcpp_action::Client<NavigateToPose>::SendGoalOptions options;
        options.goal_response_callback = [this](rclcpp_action::ClientGoalHandle<NavigateToPose>::SharedPtr goalhandle) {
            if (goalhandle){
                RCLCPP_INFO(this->get_logger(),"goal succeed be receive");
            }
        };
        options.feedback_callback = [this](rclcpp_action::ClientGoalHandle<NavigateToPose>::SharedPtr goalhandle,
        const std::shared_ptr<const NavigateToPose::Feedback> feedback) {
            (void)goalhandle;
            RCLCPP_INFO(this->get_logger(),"%.3f",feedback->distance_remaining);
        };
        options.result_callback = [this](const rclcpp_action::ClientGoalHandle<NavigateToPose>::WrappedResult result){
            if (result.code==rclcpp_action::ResultCode::SUCCEEDED)
            {
                RCLCPP_INFO(this->get_logger(),"success navigate to the pose");
            }
        };
        client_->async_send_goal(goal,options);
    }
private:
    rclcpp_action::Client<NavigateToPose>::SharedPtr client_;
};
int main(int argc,char **argv)
{
    rclcpp::init(argc,argv);
    auto client = std::make_shared<Mynode>();
    client->sendgoal();
    rclcpp::spin(client);
    rclcpp::shutdown();
}