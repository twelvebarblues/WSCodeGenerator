cmake_minimum_required(VERSION 3.5)
project(webserver)

file(GLOB_RECURSE sources src/*.cpp)

add_executable(webserver ${sources})

# these should be after the target definition
target_compile_options(webserver PUBLIC -std=c++1y -Wall -Wfloat-conversion)
target_include_directories(webserver PRIVATE include)
target_link_libraries(webserver PUBLIC PocoNet PocoFoundation PocoUtil)
