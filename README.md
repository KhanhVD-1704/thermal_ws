# Thermal Payload ROS 2 Workspace

ROS 2 Jazzy workspace for developing and testing an edge thermal-vision payload
for search-and-rescue autonomous platforms. Development is performed on an
Ubuntu 24.04.5 LTS laptop; the target Payload Box is a Raspberry Pi 4 Model B
running Raspberry Pi OS.

## Packages

- `payload_interfaces`: shared ROS 2 messages.
- `payload_sim`: simulated payload publisher and command receiver.
- `autonomous_host`: autonomous-side detection consumer.
- `payload_bringup`: launch files for integrated execution.

## Build

```bash
cd ~/thermal_ws
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

## Run the simulation

```bash
ros2 launch payload_bringup simulation.launch.py
```

The simulated payload publishes detections on `/payload/detections`, publishes
its state on `/payload/status`, and receives commands on `/payload/command`.
