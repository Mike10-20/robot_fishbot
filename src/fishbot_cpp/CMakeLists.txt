cmake_minimum_required(VERSION 3.8)
project(fishbot_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2 REQUIRED)
find_package(nav2_msgs REQUIRED)



add_executable(initialpose_cpp src/initialpose_cpp.cpp)
add_executable(dynamic_tf_listener src/dynamic_tf_listener.cpp)
add_executable(navtopose_cpp src/navtopose_cpp.cpp)


target_include_directories(initialpose_cpp PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
target_compile_features(initialpose_cpp PUBLIC c_std_99 cxx_std_17)  # Require C99 and C++17
ament_target_dependencies(
  initialpose_cpp
  "rclcpp"
  "geometry_msgs"
  "rclcpp_action"
  "tf2_ros"
  "tf2"
  "nav2_msgs"
)
ament_target_dependencies(
  dynamic_tf_listener
  "rclcpp"
  "geometry_msgs"
  "rclcpp_action"
  "tf2_ros"
  "tf2"
  "nav2_msgs"
)
ament_target_dependencies(
  navtopose_cpp
  "rclcpp"
  "geometry_msgs"
  "rclcpp_action"
  "tf2_ros"
  "tf2"
  "nav2_msgs"
)
install(TARGETS initialpose_cpp
dynamic_tf_listener
navtopose_cpp
  DESTINATION lib/${PROJECT_NAME})

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
