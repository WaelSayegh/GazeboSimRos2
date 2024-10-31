#!/bin/bash

IMAGE_NAME="itls_gazebo_simulation"
IMAGE_TAG="latest"

mkdir -p ~/.vscode-server-cache

if [ -z "${ROS_DOMAIN_ID}" ]; then
    echo "ROS_DOMAIN_ID is not set, please configure it in your .bashrc!"
    export ROS_DOMAIN_ID=1
    echo "Defaulting ROS_DOMAIN_ID to 1"
else
    echo "ROS_DOMAIN_ID is set to ${ROS_DOMAIN_ID}"
fi

docker run -it \
            --network=host \
            --privileged \
            --device=/dev/dri:/dev/dri \
            --restart unless-stopped \
            -v `pwd`:/home/user/ros2_ws \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -v /home/$USER/.vscode-server-cache:/home/user/.vscode-server \
            -v /home/$USER/.ssh:/home/user/.ssh \
            -v /dev/input:/dev/input \
            -e "DISPLAY=${DISPLAY}" \
            -e "ROS_DOMAIN_ID=${ROS_DOMAIN_ID}" \
            -e "NVIDIA_DRIVER_CAPABILITIES=all" \
            -e "QT_X11_NO_MITSHM=1" \
            --ipc=host \
            -w /home/user/ros2_ws/ \
            --name itls_gazebo_simulation \
            ${IMAGE_NAME}:${IMAGE_TAG} \
            /bin/bash