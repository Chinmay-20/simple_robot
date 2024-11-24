from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Get package directory
    pkg_share = FindPackageShare('simple_robot').find('simple_robot')
    urdf_path = os.path.join(pkg_share, 'urdf', 'simple_robot.urdf')
    world_path = os.path.join(pkg_share, 'worlds', 'obstacle_world.world')
    
    # Launch Gazebo with our world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={'world': world_path}.items()
    )
    
    # Spawn the robot
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'simple_robot', '-file', urdf_path],
        output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        spawn_robot
    ])