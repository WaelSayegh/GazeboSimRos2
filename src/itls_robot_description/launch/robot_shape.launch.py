import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node


def generate_launch_description():
    # Setup package dir
    desc_package = get_package_share_directory('itls_robot_description')
    ros_gz_sim_package = get_package_share_directory('ros_gz_sim')

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_package, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            desc_package,
            'gazebo_model',
            'without_lidar.sdf'
        ])}.items(),
    )
   


    # # Initialize Gazebo Bridge
    # gz_bridge = Node(
    #     package = "ros_ign_bridge",
    #     executable = "parameter_bridge",
    #     name = "gazebo_bridge",
    #     arguements
    # )

    # # Visualize in RViz
    # rviz = Node(
    #    package='rviz2',
    #    executable='rviz2',
    #    arguments=['-d', os.path.join(pkg_project_bringup, 'config', 'diff_drive.rviz')],
    #    condition=IfCondition(LaunchConfiguration('rviz'))
    # )

    # # Bridge ROS topics and Gazebo messages for establishing communication
    # bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     parameters=[{
    #         'config_file': os.path.join(pkg_project_bringup, 'config', 'ros_gz_example_bridge.yaml'),
    #         'qos_overrides./tf_static.publisher.durability': 'transient_local',
    #     }],
    #     output='screen'
    # )

    return LaunchDescription([
        gz_sim,
        # bridge,
        # robot_state_publisher,
        # rviz
    ])
