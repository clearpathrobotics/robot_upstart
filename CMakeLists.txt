cmake_minimum_required(VERSION 3.0.2)
project(robot_upstart)

find_package(catkin REQUIRED)

catkin_package()
catkin_python_setup()

file(GLOB SCRIPTS scripts/*)
install(PROGRAMS ${SCRIPTS} DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
install(DIRECTORY templates DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

if (CATKIN_ENABLE_TESTING)
  find_package(roslint REQUIRED)
  roslint_python()
  roslint_add_test()

  catkin_add_nosetests(test)
endif()
