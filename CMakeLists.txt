cmake_minimum_required(VERSION 3.12)
project(pygotchi)

set(CMAKE_CXX_STANDARD 14)

find_package(pybind11 REQUIRED)

pybind11_add_module(_tamagotchi src/Tamagotchi.cpp)