import espeakng
import rclpy
from rclpy.node import Node
from autopatrol_interface.srv import Speech
class Mynode(Node):
    def __init__(self):
        super().__init__("speaker_node")
        self.server = self.create_service(Speech,"speech_text",self.callback)
        self.speaker = espeakng.Speaker()
        self.speaker.voice = "zh"
    def callback(self,request,response):
        self.get_logger().info(f"reading {request.text}")
        self.speaker.say(request.text)
        self.speaker.wait()
        response.result = True
        return response
def main():
    rclpy.init()
    rclpy.spin(Mynode())
    rclpy.shutdown()