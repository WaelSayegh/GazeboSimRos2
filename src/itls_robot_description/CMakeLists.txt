cmake_minimum_required(VERSION 3.8)
project(itls_robot_description)

add_compile_options(-Wall -Wextra -Wpedantic -Werror -std=c++17)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

# Install the python module for this package
ament_python_install_package(${PROJECT_NAME})

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY config DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY urdf DESTINATION share/${PROJECT_NAME}/)
install(DIRECTORY gazebo_model DESTINATION share/${PROJECT_NAME}/)

ament_export_dependencies(rclcpp rclpy robot_state_publisher)

ament_package()
