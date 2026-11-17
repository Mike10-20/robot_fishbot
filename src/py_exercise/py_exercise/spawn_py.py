import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
class Mynode(Node):
    def __init__(self):
        super().__init__("spawn_node")
        self.declare_parameter("x",3.0)
        self.declare_parameter("y",3.0)
        self.declare_parameter("theta",0.0)
        self.declare_parameter("name","t2")
        self.client = self.create_client(Spawn,"/spawn")
        self.x = self.get_parameter("x").get_parameter_value().double_value
        self.y = self.get_parameter("y").get_parameter_value().double_value
        self.theta = self.get_parameter("theta").get_parameter_value().double_value
        self.name = self.get_parameter("name").get_parameter_value().string_value
        while(not self.client.wait_for_service(1.0)):
            self.get_logger().info("wait for server connect")
        self.get_logger().info("succeed connect server")
    def sendrequest(self):
        request = Spawn.Request()
        request.x = self.x        
        request.y = self.y        
        request.theta = self.theta        
        request.name = self.name
        self.future = self.client.call_async(request)     
def main():
    rclpy.init()
    client = Mynode()
    client.sendrequest()
    rclpy.spin_until_future_complete(client,client.future)
    try:
        result = client.future.result()
        name = result.name
        if len(name)==0:
            client.get_logger().info("name mistake")
        else:
            client.get_logger().info("succeed generate a new turtle %s" % name)
    except Exception as e:
        client.get_logger().info(str(e))

    
