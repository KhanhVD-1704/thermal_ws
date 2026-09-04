from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    fake_payload = Node(
        package='payload_sim',
        executable='fake_payload',
        name='fake_payload',
        output='screen'
    )

    detection_receiver = Node(
        package='autonomous_host',
        executable='detection_receiver',
        name='detection_receiver',
        output='screen'
    )

    return LaunchDescription([
        fake_payload,
        detection_receiver
    ])
