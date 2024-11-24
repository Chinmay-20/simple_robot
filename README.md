Installed packages

sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-gazebo-ros
sudo apt-get install ros-humble-laser-geometry ros-humble-navigation2

To run application commands

source /opt/ros/humle/setup.bash

source install/setup.bash

colcon build --packages-select simple_robot

In terminal 1
ros2 launch simple_robot robot_sim.launch.py

In terminal 2 
ros2 run simple_robot teleop_controller

In terminal 3 
rviz2

In RViz2:
Set the Fixed Frame to "base_link"
Add a LaserScan display
Set the topic to "/scan"
You should see the Lidar data as points around the robot