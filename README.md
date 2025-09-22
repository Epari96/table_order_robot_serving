# ROS2 로봇 서빙 시뮬레이션 (Table Order + POS + Nav2)

ROS2 Humble 기반의 통신 및 자율주행 시뮬레이션 시스템 프로젝트입니다.

PyQt5 기반의 테이블 주문 GUI와, 주문 처리 및 로봇 제어를 위한 POS GUI, Nav2 연동으로 서빙 로봇 흐름을 시뮬레이션합니다.  
실제 로봇 없이도 주문-수락-서빙까지의 end-to-end 로직을 검증하는 데 목적이 있습니다.

## 주요 기능

### 테이블 주문 GUI (`table_order`)
  - 주문 접수: ROS2 service 통신 `/pos/order_service` (`tors_interfaces/srv/OrderMsg` Service Client)
  - 직원 호출: ROS2 topic 통신 `/pos/call_waiter` (`std_msgs/Int32` Publish)
  - 음식 수령 확인: ROS2 service 통신 `/pos/confirm_receipt` (`std_srvs/SetBool` Service Client)
  - 동적 GUI로 장바구니 기능 구현

### POS 제어 GUI (`pos_control`)
  - 주문 수신 팝업, 주문 내역 확인
  - 결제 버튼으로 주문 내역 초기화, SQLite 연동 매출 저장/조회
  - 주문 수락/거절 → 테이블로 결과 전달
  - 로봇 제어: ROS2 action 통신 `/navigate_to_pose` (`nav2_msgs/action/NavigateToPose` Action Client)

### Dummy Nav2 서버 (`dummy_nav2_server.py`)
  - `NavigateToPose` 액션 서버 모사
  - goal 선점/취소를 CANCELED로 처리
  - 수락/성공/실패 플로우를 빠르게 테스트

### 인터페이스 (srv/msg)
  - `tors_interfaces/srv/OrderMsg` : `table_id`, `client_order_id`, `items_json`
  - `tors_interfaces/msg/OrderItem` : 메뉴/수량 등 (GUI 내부 표현 구조와 호환)

### GUI (PyQt5 / Qt Designer)
  - `TableOrder.ui`, `PosControl.ui`: ui 베이스 파일 분리로 가독성과 유지보수성 향상
  - `table_gui_widget.py`, `pos_gui_widget.py`: 동적 GUI 기능과 버튼 콜백 로직을 메인 파일에서 분리하여 코드 가독성과 유지보수성 향상
  - MultiThreadedExecutor + QThread: GUI와 ROS 노드 스레드를 분리해 안전 연동

## 실행 (Docker Compose with GUI)

### 0) 요구사항 (Requirements)
- GUI 기반 Linux OS (Ubuntu 22.04 LTS 이상 권장)
- Docker
- X11 desktop session (Wayland users: ensure XWayland is enabled)

### 1) 도커 이미지 빌드 (Build Docker Image)
```bash
# From project root (where Dockerfile is located)
docker build -t ros-humble-tors:v0.05 -f Dockerfile .
```

### 2) 컨테이너 실행 (Run Container)
```bash
docker compose up -d
```

### 3) 컨테이너 진입 (Enter Container (with Allow X11 & Prepare Environment))
```bash
# Allow X11 connections
xhost +local:docker
docker compose exec ros2-gui bash
```

### 4) 실행 (Inside Container)
Terminal A - POS GUI
```bash
# Go to workspace
cd /workspace/tors_ws

# Source ROS environment
source /opt/ros/humble/setup.bash

# Run server GUI
ros2 run pos_control pos_control
```
Terminal B - Table GUI
```bash
# Go to workspace
cd /workspace/tors_ws

# Source ROS environment
source /opt/ros/humble/setup.bash

# Run server GUI
ros2 run table_order table_order
```
Terminal C - Dummy Nav2
```bash
# Go to workspace
cd /workspace/tors_ws

# Source ROS environment
source /opt/ros/humble/setup.bash

# Run server GUI
ros2 run dummy_nav2 dummy_nav2_server
```

### 5) 실행 시나리오 (Flow Check)
1. 테이블 GUI에서 메뉴 선택 → 담기 → 주문 전송

2. POS GUI에서 수락할 때 까지 대기 → 수락 시 테이블 GUI 주문내역에 추가

3. POS GUI 주문내역에서 메뉴 확인 → 음식이 준비되면 로봇 호출

4. 로봇이 주방에 도착 → 음식 적재 → 테이블로 이동 명령

5. 테이블에서 음식 수령 후 "수령완료" 버튼 누름 → POS에서 자동으로 로봇에 복귀 명령

## 노드/토픽/서비스 개요
### Topics
 - /pos/call_waiter : std_msgs/Int32 (테이블→POS)

### Services
 - /pos/order_service : tors_interfaces/srv/OrderMsg (테이블→POS 주문)
 - /pos/confirm_receipt : std_srvs/SetBool (테이블→POS 수신확인)

### Actions (Dummy)
 - NavigateToPose : Dummy Nav2가 처리 (POS에서 버튼 → 로봇 이동 시나리오 테스트)