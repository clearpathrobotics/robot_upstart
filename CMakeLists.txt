cmake_minimum_required(VERSION 2.8.3)
project(robot_upstart)

find_package(catkin)
catkin_package()

file(GLOB SCRIPTS scripts/*)
install(PROGRAMS ${SCRIPTS} DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
install(DIRECTORY templates DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
