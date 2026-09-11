# AGENTS.md

==================================================
1. PROJECT CONTEXT
==================================================

This project supports the graduation thesis:

“NGHIÊN CỨU VÀ THIẾT KẾ MÔ-ĐUN THỊ GIÁC BIÊN THÔNG MINH
SỬ DỤNG ẢNH NHIỆT PHỤC VỤ TÌM KIẾM CỨU HỘ
TRÊN THIẾT BỊ TỰ HÀNH”

The main product is an edge-vision Payload Box for thermal perception.

Target architecture:

Thermal Camera
      ↓
Edge Computer
(selected: Raspberry Pi 4 Model B)
      ↓
Image Acquisition
      ↓
Pre-processing
      ↓
CNN Human Detection
      ↓
Post-processing
      ↓
ROS 2
      ↓
Autonomous Platform

The Payload Box is responsible for perception.

The autonomous platform is responsible for higher-level functions such as:
- decision making;
- navigation;
- mission logic;
- actuation.

Main project objectives:
- Acquire thermal images.
- Process thermal images at the edge.
- Detect humans using a CNN.
- Communicate between Payload Box and autonomous platform using ROS 2.
- Evaluate detection accuracy, FPS, latency and integration capability.

The architecture should remain modular.

The autonomous-side software should not depend on whether detections come from:
- a simulator;
- a real thermal camera;
- a real CNN pipeline;

as long as the ROS 2 interface contract remains compatible.

Currently, the real thermal camera, Raspberry Pi 4 Model B, CNN pipeline and robot/autonomous hardware have NOT been deployed.

The current laptop is only:
- the development environment;
- a ROS 2 integration test host representing the autonomous-platform side.

Do not treat the laptop itself as the autonomous vehicle.

==================================================
2. DEVELOPMENT ENVIRONMENT
==================================================

Development laptop operating system:
Ubuntu 24.04.5 LTS

Development laptop ROS version:
ROS 2 Jazzy

Payload Box target:

- Edge computer: Raspberry Pi 4 Model B.
- Operating system: Raspberry Pi OS.
- ROS version: ROS 2 Jazzy.
- The Raspberry Pi is the future real Payload Box runtime.
- Do not assume that Ubuntu-specific ROS installation steps also apply unchanged
  to Raspberry Pi OS; verify the Raspberry Pi OS installation method separately.

Workspace:

~/thermal_ws

ROS 2 environment:

source /opt/ros/jazzy/setup.bash

After the workspace has been built:

source ~/thermal_ws/install/setup.bash

Build system:

colcon

Main workspace root:

~/thermal_ws

Source directory:

~/thermal_ws/src

Before running relative-path commands, always verify the current working directory.

For builds, normally use:

cd ~/thermal_ws
source /opt/ros/jazzy/setup.bash

If install/setup.bash exists:

source ~/thermal_ws/install/setup.bash

Then run the required colcon command.

--------------------------------------------------
2.1 SELECTED THERMAL CAMERA
--------------------------------------------------

The thermal camera selected for this project is:

Waveshare Thermal-90 USB Camera

Project-relevant camera configuration:

- Thermal image resolution: 80(H) × 62(V) pixels.
- Field of view: 90° wide-angle version.
- Host connector/interface: USB Type-C (USB-C).
- The supplied connection cable is Type-C to Type-C.
- On Raspberry Pi/Linux, use the USB-camera path and the vendor USB example
  (`stream_usb.py`) as the relevant integration reference.

IMPORTANT VARIANT BOUNDARY:

- Use information for the Thermal-90 USB Camera only.
- Do NOT use the 45° basic-version field of view.
- Do NOT treat this device as the Thermal Camera HAT or Thermal-90 Camera HAT.
- Do NOT design the camera integration around the Raspberry Pi 40-pin GPIO
  header, SPI or I2C; those connections and setup steps belong to HAT variants.
- When a Waveshare page describes several variants together, verify that each
  specification or procedure applies to the Type-C, 90° USB variant before
  adding it to this project.

Official vendor references:

- Wiki: https://www.waveshare.com/wiki/Thermal_Camera_HAT
- Product page: https://www.waveshare.com/thermal-camera.htm

Selection of this model does not mean that the physical camera has already
been deployed. Until hardware integration is explicitly completed and tested,
the camera remains the selected target hardware and `payload_sim` remains the
verified integration source.

==================================================
3. CURRENT PROJECT ARCHITECTURE
==================================================

Current workspace structure:

~/thermal_ws/src/

├── payload_interfaces
├── payload_sim
├── autonomous_host
└── payload_bringup

--------------------------------------------------
3.1 payload_interfaces
--------------------------------------------------

Build type:

ament_cmake

Purpose:

Shared ROS 2 interfaces used between the Payload and external/autonomous-side software.

Current custom message:

payload_interfaces/msg/Detection

Detection.msg:

builtin_interfaces/Time stamp

bool human_detected
float32 confidence

int32 x
int32 y
int32 width
int32 height

uint32 frame_id

Current meaning:

stamp:
Detection timestamp.

human_detected:
Whether a human is detected.

confidence:
Detector confidence.

x, y, width, height:
Bounding box.

frame_id:
Currently used as an increasing frame/sequence counter.

NOTE:

The name frame_id may later be reconsidered because ROS commonly uses
frame_id for coordinate-frame identifiers in std_msgs/Header.

Do NOT rename this field unless explicitly requested or justified by a later architecture change.

--------------------------------------------------
3.2 payload_sim
--------------------------------------------------

Build type:

ament_python

Purpose:

Simulates the Payload Box before the real thermal camera + CNN + Raspberry Pi pipeline is available.

Executable:

fake_payload

Node:

/fake_payload

Current working topics include:

/payload/detections

Type:

payload_interfaces/msg/Detection

The fake detection currently simulates fields such as:

human_detected = True
confidence = 0.90

x = 50
y = 30
width = 40
height = 90

frame counter increases over time.

The current detection publishing behavior is already verified and should not be broken without a clear reason.

The simulated Payload also currently provides:

/payload/status

Type:

std_msgs/msg/String

Current status value:

RUNNING

The simulated Payload also subscribes to:

/payload/command

Type:

std_msgs/msg/String

Supported command values:

START
STOP
RESET

Commands are currently received and logged only. They do not yet change
detection or status behavior.

--------------------------------------------------
3.3 autonomous_host
--------------------------------------------------

Build type:

ament_python

Purpose:

Represents software running on the external/autonomous-platform side.

Executable:

detection_receiver

Node:

/detection_receiver

Currently subscribes to:

/payload/detections

Type:

payload_interfaces/msg/Detection

This node has already successfully received:
- human_detected;
- confidence;
- bounding box;
- frame counter.

--------------------------------------------------
3.4 payload_bringup
--------------------------------------------------

Build type:

ament_python

Purpose:

Starts the ROS 2 system using launch files.

Current launch file:

launch/simulation.launch.py

It currently launches at least:
- payload_sim / fake_payload
- autonomous_host / detection_receiver

Verified launch command:

ros2 launch payload_bringup simulation.launch.py

==================================================
4. VERIFIED BASELINE
==================================================

The following functionality has already been verified:

ROS 2 workspace                     PASS (previous verified baseline)
colcon build                        PASS

payload_interfaces                  PASS
payload_sim                         PASS
autonomous_host                     PASS
payload_bringup                     PASS

Custom Detection.msg                PASS

fake_payload publisher              PASS

/payload/detections                 PASS

detection_receiver subscriber       PASS

Custom-message communication        PASS

ROS 2 launch                        PASS

/payload/status                     PASS

/payload/command                    PASS

START / STOP / RESET reception      PASS

Current logical flow:

                  /fake_payload
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
 /payload/detections         /payload/status
 Detection                   std_msgs/msg/String
          │
          ▼
 /detection_receiver

The detection pipeline has been observed to work with matching frame values.

Example expected runtime behavior:

fake_payload:
Published detection:
human=True, confidence=0.90, frame=0

detection_receiver:
Received detection:
human=True, confidence=0.90,
bbox=(50, 30, 40, 90),
frame=0

Then frame 1 → 1, frame 2 → 2, etc.

==================================================
5. IMPORTANT RUNTIME LESSON
==================================================

This project has previously experienced duplicate ROS 2 data because an old fake_payload process was still running in another terminal.

Example symptom:

frame=0
frame=386
frame=1
frame=387
...

This did NOT mean the new implementation was necessarily broken.

It meant multiple publishers were active on the same topic.

Therefore:

If duplicate ROS 2 messages, publishers, nodes or unexpected topic behavior appear,
inspect the runtime state before modifying code.

Useful commands may include:

ros2 node list

ros2 topic list

ros2 topic info <topic> -v

ros2 node info <node>

ps

pgrep

Do not immediately blame the implementation when stale ROS 2 processes may be present.

==================================================
6. TARGET SYSTEM DIRECTION
==================================================

Long-term target software structure may evolve toward:

thermal_ws/
└── src/
    ├── payload_interfaces/
    ├── payload_sim/
    ├── payload_perception/
    ├── autonomous_host/
    └── payload_bringup/

Possible roles:

payload_interfaces:
Shared ROS 2 interfaces.

payload_sim:
Simulation and interface testing.

payload_perception:
Future real thermal-camera + preprocessing + CNN + post-processing + ROS 2 publishing pipeline.

autonomous_host:
Consumer/control software on the autonomous-platform side.

payload_bringup:
Launch and configuration.

Do NOT create future packages only because they are listed here.

Only implement them when the current task actually requires them.

==================================================
7. ROS 2 INTERFACE DIRECTION
==================================================

Current confirmed interfaces:

Payload → External / Autonomous side

/payload/detections
/payload/status

External / Autonomous side → Payload

/payload/command

Possible future interfaces may include:

/payload/thermal/image

These are architecture directions, not automatic implementation requirements.

Do not implement future interfaces unless requested.

The Payload should behave as an independent ROS 2 perception module.

The external/autonomous software should remain as independent as possible from the internal implementation of the Payload.

Example:

CURRENT:

fake_payload
      ↓
/payload/detections
      ↓
detection_receiver

FUTURE:

Thermal Camera
      ↓
Pre-processing
      ↓
CNN
      ↓
thermal_detector
      ↓
/payload/detections
      ↓
detection_receiver

If the interface contract remains stable, the autonomous-side consumer should not require unnecessary rewriting.

==================================================
8. DEVELOPMENT PRINCIPLES
==================================================

Before modifying code:

- Inspect the actual filesystem and current implementation.
- Treat the current repository/filesystem as the source of truth.
- Do not assume a file still matches old documentation or previous prompts.

When developing:

- Preserve already working functionality.
- Prefer small, modular changes.
- Modify only files that are actually required.
- Avoid unnecessary large refactors.
- Do not rename working topics, packages, executables or interfaces without a justified reason.
- Do not implement camera, CNN, Raspberry Pi or robot functionality unless the current task requires it.
- Avoid sudo unless truly necessary.
- Avoid installing new system dependencies unless required.
- Do not over-engineer.
- Prefer a simple working implementation before a complex architecture.
- Keep simulation code and future hardware code conceptually separated.
- Clearly distinguish verified functionality from planned functionality.

The Agent is allowed to choose the implementation approach needed to achieve the user's goal.

The Agent may:
- inspect files;
- inspect ROS 2 graph/runtime;
- select which files require modification;
- create small supporting files when justified;
- build packages;
- run tests;
- use ROS 2 CLI tools;
- debug task-related failures;
- fix small blocking issues directly related to the current task.

Do not rigidly follow a predefined command sequence if another safe and appropriate method is better.

==================================================
9. BUILD AND TEST RULES
==================================================

After meaningful code changes:

1. Build the affected package(s).

2. Source the ROS 2 environment.

3. Source the workspace.

4. Run appropriate tests.

5. If the change affects runtime ROS 2 communication, verify it at runtime.

If a build or test fails:

- Read the actual error.
- Identify the root cause.
- Fix the root cause.
- Rebuild.
- Retest.

Do not claim PASS without verification.

Generated directories:

build/
install/
log/

should not be treated as source code.

Do not manually modify generated build/install files as a normal development approach.

==================================================
10. GIT / MULTI-MACHINE DIRECTION
==================================================

Development is performed on a laptop running Ubuntu 24.04.5 LTS + ROS 2 Jazzy.

The target Payload Box is a Raspberry Pi 4 Model B running Raspberry Pi OS +
ROS 2 Jazzy. Keep laptop development and Raspberry Pi deployment instructions
separate where their operating systems require different setup steps.

The source code may later be synchronized to another development machine using Git.

Generated ROS 2 directories should normally not be version-controlled:

build/
install/
log/

Source code, launch files, package manifests, interfaces and relevant configuration should be version-controlled.

Do not make home-machine migration or ROS-version migration block current development unless explicitly requested.

==================================================
11. PROJECT METRICS FOR LATER EVALUATION
==================================================

Future experimental evaluation may include:

- Detection accuracy
- FPS
- Inference time
- CPU usage
- RAM usage
- Temperature
- Power consumption if measurable
- Communication latency
- End-to-end latency

Conceptually:

T_total =
    T_capture
  + T_pre
  + T_inference
  + T_post
  + T_communication

Do not implement the complete metrics framework unless the current task requires it.

==================================================
12. PROJECT ROADMAP
==================================================

Long-term roadmap:

PHASE 0
System Requirements

PHASE 1
Hardware Selection

PHASE 2
Thermal Camera Bring-up

PHASE 3
Thermal Image Pipeline

PHASE 4
CNN Human Detection

PHASE 5
Edge Optimization

PHASE 6
ROS 2 Integration

PHASE 7
Complete Payload Box

PHASE 8
Autonomous Platform Integration

PHASE 9
Experiments & Evaluation

PHASE 10
Report + Final Demo

Current development intentionally performs ROS 2 integration early using simulation/interface-first development.

Current practical direction:

Laptop Ubuntu 24.04.5 LTS
      ↓
ROS 2 Jazzy
      ↓
ROS 2 Nodes / Topics / Pub-Sub
      ↓
Workspace
      ↓
Fake Payload
      ↓
Autonomous-side software
      ↓
Custom Interfaces
      ↓
Launch
      ↓
Payload status / control interfaces
      ↓
Later real Payload implementation

The roadmap provides context only.

Do NOT automatically execute the next roadmap phase after finishing the current task.

==================================================
13. DYNAMIC TASK UPDATE RULE
==================================================

The newest user request entered directly in Codex CLI is the source of truth for the CURRENT TASK.

For every new user request:

1. Read this AGENTS.md.

2. Inspect the relevant current project state.

3. Treat the actual filesystem and verified runtime state as more authoritative than stale text in this file.

4. Update the "CURRENT TASK" section below so it reflects the newest user request accurately and concisely.

5. Set:

Status: IN_PROGRESS

before implementation begins.

6. If inspection shows that "CURRENT PROJECT STATE" is stale,
update it using only verified facts.

7. Do NOT rewrite stable project context, architecture or development rules unless:
- the user explicitly requests the change; or
- the completed implementation genuinely changes a stable project decision.

8. After updating AGENTS.md:

CONTINUE EXECUTING THE USER'S TASK IMMEDIATELY.

Do not stop merely because AGENTS.md was updated.

Do not ask:
“Do you want me to continue?”

when the user's request is already clear.

9. Use the current task as a goal, not as a rigid script.

The Agent may choose the appropriate:
- implementation;
- files;
- ROS 2 inspection commands;
- tests;
- debug procedure.

10. If a task-related error occurs:
- investigate;
- diagnose;
- fix;
- build/test again;

when this can be done safely within the task.

11. Do not automatically continue into unrelated future work.

12. When the task is complete:

- update CURRENT PROJECT STATE if a new stable milestone was actually verified;
- set CURRENT TASK Status to COMPLETED;
- retain a concise description of what was completed.

13. Keep AGENTS.md concise and useful.

Do NOT store transient information such as:
- temporary PIDs;
- long command output;
- full logs;
- one-time debugging noise;
- already-resolved transient errors;
- frame numbers from individual test runs.

==================================================
14. CURRENT PROJECT STATE
==================================================

Current development environment:

- Laptop operating system: Ubuntu 24.04.5 LTS.
- ROS distribution: ROS 2 Jazzy.
- Workspace: ~/thermal_ws.

Target Payload Box environment:

- Edge computer: Raspberry Pi 4 Model B.
- Operating system: Raspberry Pi OS.
- ROS distribution: ROS 2 Jazzy.
- Deployment and runtime verification on the Raspberry Pi are still pending.

Verified packages:

- payload_interfaces
- payload_sim
- autonomous_host
- payload_bringup

Verified interfaces:

- payload_interfaces/msg/Detection
- /payload/detections
- /payload/status
- /payload/command

Verified functionality:

- fake_payload publishes Detection messages.
- fake_payload publishes Payload status.
- detection_receiver receives Detection messages.
- ROS 2 custom message communication works.
- simulation.launch.py starts the simulated ROS 2 system.
- Detection publisher/subscriber pipeline works.
- /payload/status has been implemented and tested successfully.
- fake_payload subscribes to /payload/command using std_msgs/msg/String.
- fake_payload receives and logs START, STOP and RESET commands.
- Command reception does not currently change detection or status behavior.

Current logical architecture:

                 fake_payload
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
 /payload/detections       /payload/status
 Detection                 std_msgs/msg/String
          │
          ▼
 detection_receiver

 autonomous-side publisher
          │
          ▼
 /payload/command
 std_msgs/msg/String
          │
          ▼
     fake_payload

Real hardware status:

- Raspberry Pi 4 Model B: selected, not yet deployed or runtime-verified.
- Thermal camera: Waveshare Thermal-90 USB Camera selected, not yet deployed.
- CNN detector: not yet integrated into Payload runtime.
- Physical autonomous platform: not yet integrated.

==================================================
15. CURRENT TASK
==================================================

Status: COMPLETED

Update the documented hardware and software environment decisions:

- Payload edge computer: Raspberry Pi 4 Model B.
- Payload operating system: Raspberry Pi OS.
- Development laptop: Ubuntu 24.04.5 LTS.
- ROS distribution for laptop and Payload: ROS 2 Jazzy.
- Preserve the distinction between the development laptop and the real Payload Box.

Documentation updated. Runtime verification on the new Jazzy environments is
still pending and must not be reported as complete until actually tested.

==================================================
16. COMPLETION REPORT STYLE
==================================================

After completing a task, report briefly:

CHANGED
- What was changed.
- Which important files were modified.

WHY
- Why the changes were needed.

TEST
- What important build/runtime tests were performed.

RESULT
- PASS or FAIL.
- Any remaining issue that actually matters.

Keep the report concise.

The user is learning ROS 2 while developing this thesis, so include a short explanation of the relevant ROS 2 concept when useful.

Do not overwhelm the user with unnecessary theory after every task.
