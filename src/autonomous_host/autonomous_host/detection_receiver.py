import rclpy
from rclpy.node import Node
from payload_interfaces.msg import Detection


class DetectionReceiver(Node):

    def __init__(self):
        super().__init__('detection_receiver')

        self.subscription = self.create_subscription(
            Detection,
            '/payload/detections',
            self.detection_callback,
            10
        )

    def detection_callback(self, msg):
        self.get_logger().info(
            f'Received detection: '
            f'human={msg.human_detected}, '
            f'confidence={msg.confidence:.2f}, '
            f'bbox=({msg.x}, {msg.y}, {msg.width}, {msg.height}), '
            f'frame={msg.frame_id}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = DetectionReceiver()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()