# table_order_robot_serving
[ROS2] Autonomous serving simulation with TurtleBot3 in Gazebo: table order & POS control

## Run (Docker Compose with GUI)

### 0) Requirements
- GUI based Linux OS(Recommanded over ubuntu 22.04 LTS)
- Docker
- X11 desktop session (Wayland users: ensure XWayland is enabled)

### 1) Build Image
```bash
# From project root (where Dockerfile is located)
docker build -t ros-humble-tors:v0.05 -f Dockerfile .
```

### 2) Run Container
```bash
docker compose up -d
```

### 3) Enter Container (with Allow X11 & Prepare Environment)
```bash
# Allow X11 connections
xhost +local:docker
docker compose exec ros2-gui bash
```

### 4) Inside Container
```bash
# Go to workspace
cd /workspace/tors_ws

# Source ROS environment
source /opt/ros/humble/setup.bash

# Run server GUI
ros2 run table_order_gui pos_server_gui

# In another terminal/container shell, run client GUI
ros2 run table_order_gui table_client_gui
```

### 5) Flow Check
1. Start Server GUI → shows waiting state.

2. Start Client GUI → enter table ID, food, and quantity → press Send.

3. Server GUI displays order details → click Accept or Reject.

4. Client GUI updates status: “Accepted” or “Rejected”.