# 베이스 이미지
FROM ros:humble-ros-base-jammy

# 환경변수
ENV DEBIAN_FRONTEND=noninteractive

# 필수 패키지 설치
RUN apt update && apt install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-rosinstall-generator \
    python3-vcstool \
    lsb-release \
    build-essential \
    git \
    curl \
    wget \
    nano \
    fonts-nanum \
# OpenGL 및 X11 관련 패키지
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    x11-apps \
# ROS2 GUI 패키지 설치
    ros-humble-rviz2 \
    ros-humble-rqt \
    ros-humble-rqt-common-plugins \
    ros-humble-tf2-tools \
    python3-pyqt5 \
    ros-humble-rclpy \
# Gazebo 설치
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-gazebo-plugins \
# navigation2 설치
    ros-humble-nav2-map-server \
    ros-humble-nav2-bringup \
# TurtleBot3 설치
    ros-humble-dynamixel-sdk \
    ros-humble-turtlebot3-gazebo \
    ros-humble-turtlebot3-navigation2 \
    && rm -rf /var/lib/apt/lists/*

# rosdep 초기화
RUN rosdep init || true
RUN rosdep update

# 작업 디렉토리
WORKDIR /workspace

# 필요하면 ROS 환경 소스
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "export TURTLEBOT3_MODEL=waffle_pi" >> ~/.bashrc
RUN echo "export ROS_LOCALHOST_ONLY=0" >> ~/.bashrc

# 컨테이너 실행 시 기본 명령
CMD ["bash"]
