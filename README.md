# ROS2 로봇 서빙 시뮬레이션 (Table Order + POS + Nav2)

ROS2 Humble 기반의 통신 및 자율주행 시뮬레이션 프로젝트입니다.

하나의 시스템 안에서 ROS2의 topic, service, action 통신을 모두 구현하고, Gazebo와 Navigation2를 활용해 자율주행을 시뮬레이션함으로써 ROS2 프레임워크와 자율주행 로직에 대한 이해도를 높이는 것을 목표로 했습니다.
 
PyQt5 기반의 테이블오더 GUI와, 주문 확인·결제 및 로봇 제어를 위한 POS GUI를 실제 서비스와 유사하게 구현하였습니다. 커스텀 가능한 gazebo 맵을 활용하여 실제 장소와 로봇 없이도 **주문-수락-서빙-복귀**까지의 end-to-end 로직을 검증할 수 있습니다.

## 주요 기능

### 테이블오더 GUI (`table_order.py, table_gui_widget.py`)
  - 음식 주문
    - 커스텀 인터페이스(`tors_interfaces/srv/OrderMsg`)를 통해 주문 내역(메뉴, 수량) 전송
    - 안정적인 전송을 위해 Service Client 방식 사용 (`/pos/order_service`)
    - 주문이 접수·거절될 때까지 팝업창 유지
  - 음식 수령 확인
    - 로봇 복귀 명령을 트리거하기 위해 POS로 확인 메시지 전송 (`std_srvs/SetBool`)
    - Service Client 방식 사용 (`/pos/confirm_receipt`)
  - 직원 호출
    - 직원 호출 메시지를 POS로 전송 (`std_msgs/Int32`)
    - Topic Publisher 사용 (`/pos/call_waiter`)
  - 주문 내역
    - 접수된 주문을 저장하고, 주문 총액을 자동 계산
  - 동적 GUI
    - 메뉴 버튼을 누르면 장바구니에 시각적으로 추가되는 기능 구현
    - 주문이 접수되면 장바구니 자동 초기화

### POS 제어 GUI (`pos_control.py`, `pos_gui_widget.py`)
  - 주문 수신
    - 테이블에서 전송한 주문 요청(`tors_interfaces/srv/OrderMsg`)을 Service Server(`/pos/order_service`)에서 처리
    - 주문 도착 시 팝업창 표시 → 사용자가 수락/거절 결정
    - 수락 시 해당 테이블의 주문 내역에 기록
  - 주문 내역 관리
    - 테이블별 주문 내역 저장 및 누적
    - 선택된 테이블의 주문 내역을 실시간으로 표시
    - 결제 시 주문 내역 DB 기록 및 초기화
  - 결제 및 매출 관리
    - SQLite(`pos_orders.db`) 연동
    - 결제 완료 시 주문 내역을 DB에 저장 (`orders` 테이블: id, table_id, items_json, created_at)
    - 매출 내역 조회 기능 제공 (최근 주문 리스트 출력)
  - 직원 호출 처리
    - 테이블 GUI에서 `/pos/call_waiter` (`std_msgs/Int32`) 수신 → 해당 테이블 버튼 색상 변경
  - 음식 수령 확인 처리
    - 테이블 GUI에서 `/pos/confirm_receipt` (`std_srvs/SetBool`) 수신
    - 메세지 수신 시 로봇 호출 버튼이 자동 실행되어 복귀 처리
  - 로봇 제어
    - `/navigate_to_pose` (`nav2_msgs/action/NavigateToPose`) 액션 클라이언트로 이동 명령 전송
    - 호출, 충전, 테이블별 이동 제어
    - Emergency Stop 버튼으로 모든 goal 취소(`cancel_goal_async`) 및 정지 명령 발행(`/cmd_vel zero twist`)
  - 동적 GUI
    - 로봇 선택 버튼(서빙로봇1/2) 토글 가능
    - 테이블 상태 버튼(주문 대기, 서빙 중, 결제 완료 등) 실시간 반영
    - 이동 중/도착/중지/긴급정지 상태에 따라 버튼 색상 자동 변경

### Gazebo 시뮬레이션 환경
  - 환경 구성
    - `restaurant.launch.py` 실행 시 `gazebo`를 실행하며 `restaurant.world` 로드
    - TurtleBot3가 레스토랑 맵에 스폰되고, `gazebo_ros` 및 `robot_state_publisher`와 연동
  - 레스토랑 맵 (`restaurant.world`)
    - 식당 구조를 반영한 커스텀 월드 파일
    - 테이블·벽체·통로 등 실제 서비스 환경과 유사한 형태로 구성
  - 활용 목적
    - 실제 로봇 없이 주문 → 수락 → 서빙 end-to-end 로직을 검증 가능
    - 다양한 맵 수정·확장을 통해 서비스 환경을 손쉽게 재현 가능

### 커스텀 인터페이스 (`tors_interfaces/srv/OrderMsg`)
  - `Request`
    - `int32 table_id`
    - `string client_order_id`
    - `string items_json`
  - `Response`
    - `bool accepted`
    - `string message`

### GUI (PyQt5 / Qt Designer)
  - `TableOrder.ui`, `PosControl.ui`: UI 베이스 파일 분리로 가독성과 유지보수성 향상
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
docker compose exec ros2_gui_tors bash
```

### 4) 실행 (Inside Container)
컨테이너 내부와 연결된 4개의 터미널 필요

#### Terminal A - POS GUI
```bash
# Go to workspace
cd /workspace/tors_ws

# Source ROS environment
source install/setup.bash

# Run server GUI
ros2 run pos_control pos_control
```
#### Terminal B - Table GUI
```bash
# Go to workspace
cd /workspace/tors_ws

# Source ROS environment
source install/setup.bash

# Run server GUI
ros2 run table_order table_order
```
#### Terminal C - Gazebo (restaurant.world)
```bash
# launch gazebo
ros2 launch turtlebot3_gazebo restaurant.launch.py
```

#### Terminal D - Nav2
```bash
# launch Nav2 with map
ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=/workspace/map.yaml
```

### 5) 실행 시나리오 (Flow Check)
1. 테이블 GUI에서 메뉴 선택 → 담기 → 주문 전송

2. POS GUI에서 수락할 때까지 대기 → 수락 시 Table Order의 주문내역 버튼을 누르면 확인 가능

3. 주문 수락 시 POS의 TABLE STATUS 하단 주문내역에 추가(테이블 버튼을 눌러 테이블 별로 확인 가능)

4. POS GUI 주문내역에서 메뉴 확인 → 음식이 준비되면 로봇 호출(서빙로봇1/2 버튼 -> 로봇 호출 버튼)

5. 로봇이 주방에 도착 → 음식 적재 → 테이블로 이동 명령(ROBOT CONTROL 하단 테이블 버튼)

6. 테이블에서 음식 수령 후 "수령완료" 버튼 누름 → POS에서 자동으로 로봇에 복귀 명령 전송