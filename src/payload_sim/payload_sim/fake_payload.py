import rclpy
from rclpy.node import Node
from payload_interfaces.msg import Detection
from std_msgs.msg import String


class FakePayload(Node):

    def __init__(self):
        super().__init__('fake_payload')

        self.publisher_ = self.create_publisher(
            Detection,
            '/payload/detections',
            10
        )

        self.status_publisher = self.create_publisher(
            String,
            '/payload/status',
            10
        )

        self.command_subscription = self.create_subscription(
            String,
            '/payload/command',
            self.command_callback,
            10
        )

        self.timer = self.create_timer(
            1.0,
            self.publish_detection
        )

        self.status_timer = self.create_timer(
            2.0,
            self.publish_status
        )

        self.count = 0

    def publish_detection(self):
        msg = Detection()

        msg.stamp = self.get_clock().now().to_msg()

        msg.human_detected = True
        msg.confidence = 0.90

        msg.x = 50
        msg.y = 30
        msg.width = 40
        msg.height = 90

        msg.frame_id = self.count

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Published detection: '
            f'human={msg.human_detected}, '
            f'confidence={msg.confidence:.2f}, '
            f'frame={msg.frame_id}'
        )

        self.count += 1

    def publish_status(self):
        msg = String()
        msg.data = 'RUNNING'

        self.status_publisher.publish(msg)

        self.get_logger().info(
            f'Published status: {msg.data}'
        )

    def command_callback(self, msg):
        if msg.data in ('START', 'STOP', 'RESET'):
            self.get_logger().info(
                f'Received command: {msg.data}'
            )
        else:
            self.get_logger().warning(
                f'Unsupported command: {msg.data}'
            )


def main(args=None):
    rclpy.init(args=args)

    node = FakePayload()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
