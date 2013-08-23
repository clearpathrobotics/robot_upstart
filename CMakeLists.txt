cmake_minimum_required(VERSION 2.8.3)
project(upstart)

find_package(catkin)
catkin_package()

###########
## Build ##
###########

set(TMPLS tmpl/start tmpl/stop tmpl/job_conf)
set(TMPLS_GEN)

foreach(TMPL ${TMPLS}) 
  add_custom_command(
    OUTPUT ${PROJECT_BINARY_DIR}/${TMPL}_gen
    DEPENDS ${PROJECT_SOURCE_DIR}/${TMPL}
    COMMAND mkdir -p tmpl
    COMMAND rosrun ${PROJECT_NAME} mktmpl ${PROJECT_SOURCE_DIR}/${TMPL} ${TMPL}_gen
  )
list(APPEND TMPLS_GEN ${PROJECT_BINARY_DIR}/${TMPL}_gen)
endforeach(TMPL)

add_custom_command(
  WORKING_DIRECTORY ${CATKIN_DEVEL_PREFIX}
  OUTPUT ${CATKIN_PACKAGE_BIN_DESTINATION}/tmpl
  DEPENDS ${TMPLS_GEN}
  COMMAND ${CMAKE_COMMAND} -E copy_directory 
    ${PROJECT_BINARY_DIR}/tmpl 
    ${CATKIN_PACKAGE_BIN_DESTINATION}/tmpl
)

add_custom_target(${PROJECT_NAME}_tmpl ALL
  WORKING_DIRECTORY ${CATKIN_DEVEL_PREFIX}
  DEPENDS ${CATKIN_PACKAGE_BIN_DESTINATION}/tmpl
)

#############
## Install ##
#############

file(GLOB SCRIPTS ${PROJECT_SOURCE_DIR}/scripts/*)
install(PROGRAMS ${SCRIPTS} ${TMPLS_GEN}
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

