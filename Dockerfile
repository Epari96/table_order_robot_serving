# version 0.04 (desktop base)

FROM osrf/ros:humble-desktop-jammy
ENV DEBIAN_FRONTEND=noninteractive

# 필수/개발 유틸 + sudo(NOPASSWD) + PyQt5 + X11 의존성 + Gazebo/TB3
RUN apt update && apt install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-rosinstall-generator \
    python3-vcstool \
    lsb-release \
    build-essential \
    git curl wget nano gedit fonts-nanum \
    python3-pyqt5 \
    libxkbcommon-x11-0 libxcb-xinerama0 \
    libgl1-mesa-glx libgl1-mesa-dri x11-apps \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-gazebo-plugins \
    ros-humble-dynamixel-sdk \
    ros-humble-turtlebot3-gazebo \
    ros-humble-turtlebot3-navigation2 \
 && rm -rf /var/lib/apt/lists/*

# rosdep 초기화
RUN rosdep init || true && rosdep update

# 작업 디렉토리
WORKDIR /workspace

# 사용자 생성(기본 1000:1000)
ARG USERNAME=humble
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid ${USER_GID} ${USERNAME} \
 && useradd -m -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} ${USERNAME}

# 모든 인터랙티브 bash에서 ROS/Gazebo 환경 로드
RUN bash -lc 'printf "%s\n" \
  "source /opt/ros/humble/setup.bash" \
  "export TURTLEBOT3_MODEL=waffle_pi" \
  "export ROS_LOCALHOST_ONLY=0" \
# Gazebo 및 TurtleBot3 워크스페이스가 존재하면 로드
  "[ -f /usr/share/gazebo/setup.sh ] && source /usr/share/gazebo/setup.sh" \
  "[ -f /workspace/turtlebot3_ws/install/local_setup.bash ] && source /workspace/turtlebot3_ws/install/local_setup.bash" \
  >> /etc/bash.bashrc'

USER humble
CMD ["bash"]
