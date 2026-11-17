#include "rclcpp/rclcpp.hpp"
#include "turtlesim/srv/spawn.hpp"
using turtlesim::srv::Spawn;
using namespace std;
using namespace std::chrono_literals;
class Mynode:public rclcpp::Node
{
public:
  Mynode():Node("spawn_cpp_node")
  {
    this->declare_parameter("x",5.0);
    this->declare_parameter("y",5.0);
    this->declare_parameter("theta",0.0);
    this->declare_parameter("name","t2");
    x = this->get_parameter("x").as_double();
    y = this->get_parameter("y").as_double();
    theta = this->get_parameter("theta").as_double();
    name = this->get_parameter("name").as_string();
    client_ = this->create_client<Spawn>("/spawn");
  }
  bool connect()
  {
    while (!client_->wait_for_service(1s))
    {
      if (!rclcpp::ok())
      {
        RCLCPP_INFO(rclcpp::get_logger("rclcpp"),"client quit");
        return false;
      }
      RCLCPP_INFO(this->get_logger(),"wait for server connect");
    }
    return true;
  }
  
  rclcpp::Client<Spawn>::FutureAndRequestId sendrequest()
  {
    auto request = std::make_shared<Spawn::Request>();
    request->x = x;
    request->y = y;
    request->theta = theta;
    request->name = name;
    return client_->async_send_request(request);
  }
private:
  float x,y,theta;
  string name;
  rclcpp::Client<Spawn>::SharedPtr client_;
};
int main(int argc,char **argv)
{
  rclcpp::init(argc,argv);
  auto client_ = std::make_shared<Mynode>();
  if(!client_->connect())
  {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"),"failed to connect server");
    return 0;
  }
  else
  {
    RCLCPP_INFO(client_->get_logger(),"succeed connect server");
  }
  auto future = client_->sendrequest();
  auto a = rclcpp::spin_until_future_complete(client_,future);
  if (a==rclcpp::FutureReturnCode::SUCCESS)
  {
    auto name = future.get()->name;
    if(name.empty())
    {
      RCLCPP_ERROR(client_->get_logger(),"failed to generate a new turtle");
      return 0;
    }
    RCLCPP_INFO(client_->get_logger(),"success establish a turtle that name is %s",future.get()->name.c_str());
  }
  else{
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"),"failed to generate a new turtle***");

  }

}