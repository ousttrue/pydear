# project
cmake_minimum_required(VERSION 3.20.0)
project(impl VERSION 0.1.0)

# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/Debug/lib)
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/Debug/lib)
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/Debug/bin)
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/Release/lib)
# set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/Release/lib)
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/Release/bin)
set(CMAKE_CXX_STANDARD 17)
add_compile_options("$<$<C_COMPILER_ID:MSVC>:/utf-8>")
add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")
add_definitions(-DNOMINMAX)

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  add_compile_options(/wd4996)
endif()

# target
add_library(
  ${PROJECT_NAME} SHARED
  cpp_src/impl.cpp
  #
  _external/imgui/imgui.cpp
  _external/imgui/imgui_widgets.cpp
  _external/imgui/imgui_draw.cpp
  _external/imgui/imgui_tables.cpp
  _external/imgui/imgui_demo.cpp
  _external/imnodes/imnodes.cpp
  _external/picovg/src/nanovg.cpp)
set(Python3_FIND_REGISTRY FIRST)
find_package(Python3 REQUIRED COMPONENTS Development)
target_include_directories(
  ${PROJECT_NAME}
  PRIVATE 
          _external/imgui
          _external/imnodes
          _external/picovg/src
          ${Python3_INCLUDE_DIRS})
target_compile_definitions(
  ${PROJECT_NAME}
  PRIVATE GLEW_BUILD GLEW_STATIC NANOVG_GL3_IMPLEMENTATION
          "$<$<CXX_COMPILER_ID:MSVC>:_WIN32>"
          "$<$<CXX_COMPILER_ID:MSVC>:NOMINMAX>")
if(WIN32)
  target_link_libraries(${PROJECT_NAME} PUBLIC Advapi32.lib OPENGL32.lib
                                               GLU32.lib)
  set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".pyd")
else(WIN32)
  set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")
  target_compile_options(${PROJECT_NAME} PRIVATE "-fpermissive")
endif(WIN32)
target_link_directories(${PROJECT_NAME} PUBLIC ${Python3_LIBRARY_DIRS})
