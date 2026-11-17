cmake_minimum_required(VERSION 3.8)
project(fishbot_plugin)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(pluginlib REQUIRED)
find_package(nav2_core REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav2_core REQUIRED)
find_package(nav2_costmap_2d REQUIRED)
find_package(nav2_util REQUIRED)
find_package(nav_msgs REQUIRED)







include_directories(include)

add_library(nav2_custom_planner SHARED src/nav2_custom_planner.cpp)
add_library(nav2_custom_controller SHARED src/nav2_custom_controller.cpp)

ament_target_dependencies(nav2_custom_planner
pluginlib
geometry_msgs
rclcpp
nav2_core
nav2_util
nav2_costmap_2d
nav_msgs)
ament_target_dependencies(nav2_custom_controller
pluginlib
geometry_msgs
rclcpp
nav2_core
nav2_util
nav2_costmap_2d
nav_msgs)
install(TARGETS nav2_custom_planner
ARCHIVE DESTINATION lib 
LIBRARY DESTINATION lib 
RUNTIME DESTINATION lib/${PROJECT_NAME})
install(TARGETS nav2_custom_controller
ARCHIVE DESTINATION lib 
LIBRARY DESTINATION lib 
RUNTIME DESTINATION lib/${PROJECT_NAME})

pluginlib_export_plugin_description_file(nav2_core custom_planner.xml)
pluginlib_export_plugin_description_file(nav2_core custom_controller.xml)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
