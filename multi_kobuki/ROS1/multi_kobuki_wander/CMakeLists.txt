cmake_minimum_required(VERSION 3.0.2)
project(multi_kobuki_wander)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  kobuki_msgs
  rospy
)

catkin_package()
