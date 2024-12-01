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
    urdf_path = os.path.join(pkg_share, 'urdf', 'planar_movement_robot.urdf')
    world_path = os.path.join(pkg_share, 'worlds', 'room_world.world')
    
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
    arguments=[
        '-entity', 'simple_robot',
        '-file', urdf_path,
        '-x', '0.0',   # Center X coordinate
        '-y', '0.0',   # Center Y coordinate
        '-z', '0.15',  # Slightly above the floor to prevent clipping
        '-R', '0.0',   # Roll
        '-P', '0.0',   # Pitch
        '-Y', '0.0'    # Yaw (rotation around Z axis)
    ],
    output='screen'
    )
    
    return LaunchDescription([
        gazebo,
        spawn_robot
    ])