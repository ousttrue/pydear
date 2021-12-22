# project
cmake_minimum_required(VERSION 3.20.0)
project(imgui VERSION 0.1.0)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/Debug/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/Debug/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_BINARY_DIR}/Debug/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/Release/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/Release/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/Release/bin)
set(CMAKE_CXX_STANDARD 17)
add_definitions(-DNOMINMAX)

if("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
  add_compile_options(/wd4996)
endif()

# target
add_library(
  ${PROJECT_NAME}
  _external/imgui/imgui.cpp
  _external/imgui/imgui_widgets.cpp
  _external/imgui/imgui_draw.cpp
  _external/imgui/imgui_tables.cpp
  _external/imgui/imgui_demo.cpp
  _external/ImFileDialog/ImFileDialog.cpp
  _external/ImFileDialogWrap.cpp
  _external/imnodes/imnodes.cpp
  _external/ImGuizmo/ImGuizmo.cpp
  _external/ImGuizmo/GraphEditor.cpp
  _external/ImGuizmo/ImCurveEdit.cpp
  _external/ImGuizmo/ImGradient.cpp
  _external/ImGuizmo/ImSequencer.cpp)
target_include_directories(${PROJECT_NAME} PRIVATE _external _external/imgui
                                                   _external/stb)
target_link_libraries(${PROJECT_NAME} PUBLIC Advapi32.lib)
