import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command

from launch_ros.actions import Node


def generate_launch_description():
    # Setup packages dir
    desc_package = get_package_share_directory('itls_robot_description')
    ros_gz_sim_package = get_package_share_directory('ros_gz_sim')

    # Set the path to the URDF file
    urdf_model = os.path.join(desc_package, "urdf/itls_main.urdf.xacro")
    robot_desc_config = Command(['xacro ', urdf_model, ' sim_mode:=true'])
    robot_desc_param = {'robot_description': robot_desc_config, 'use_sim_time': True}

    # Publishes the robot description, excluding joints that can be calibrated at runtime
    robot_state_publisher_node = Node(
        name="robot_state_publisher",
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_desc_param],
    )

    # Setup to launch the simulator and Gazebo world
    sdf_file = PathJoinSubstitution([desc_package, 'gazebo_model', 'container.world'])
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_package, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': ['-r -v4 ', sdf_file], 'on_exit_shutdown': 'true'}.items(),
    )
    
    # Run spawner node from gazebo sim package
    gz_spawner = Node(package='ros_gz_sim', executable='create',
        arguments=['-topic', 'robot_description', '-name', 'itls_robot_gz', '-z', '0.14'],
        output='screen')

    # Initialize Gazebo Bridge
    gz_bridge_config = os.path.join(desc_package, 'config', 'gazebo_bridge_config.yaml')
    gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="gazebo_bridge",
        parameters=[{
            'config_file': gz_bridge_config,
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher_node,
        gz_sim,
        gz_spawner,
        gz_bridge,
    ])
