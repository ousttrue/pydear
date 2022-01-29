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
  # _external/ImFileDialog/ImFileDialog.cpp
  # _external/ImFileDialogWrap.cpp
  _external/imnodes/imnodes.cpp
  _external/ImGuizmo/ImGuizmo.cpp
  _external/ImGuizmo/GraphEditor.cpp
  _external/ImGuizmo/ImCurveEdit.cpp
  _external/ImGuizmo/ImGradient.cpp
  _external/ImGuizmo/ImSequencer.cpp
  _external/tinygizmo/tinygizmo/tiny-gizmo.cpp
  _external/nanovg/src/nanovg.c
  _external/glew-2.1.0/src/glew.c
  # _external/glew-2.1.0/src/glewinfo.c
  _external/glew-2.1.0/src/visualinfo.c)
target_include_directories(
  ${PROJECT_NAME}
  PRIVATE _external
          _external/imgui
          # _external/stb
          _external/tinygizmo/tinygizmo
          _external/glew-2.1.0/include
          _external
          _external/imnodes
          _external/nanovg/src
          _external/glew-2.1.0/include/GL
          C:/Python310/Include)
target_compile_definitions(
  ${PROJECT_NAME} PRIVATE GLEW_BUILD GLEW_STATIC NANOVG_GL3_IMPLEMENTATION
                          _WIN32 NOMINMAX)
target_link_libraries(${PROJECT_NAME} PUBLIC Advapi32.lib OPENGL32.lib
                                             GLU32.lib)
target_link_directories(${PROJECT_NAME} PUBLIC C:/Python310/libs)

if(WIN32)
  set_target_properties(${PROJECT_NAME} PROPERTIES SUFFIX ".pyd")
endif(WIN32)
