cmake_minimum_required(VERSION 3.26)
project(statparser)

set(CMAKE_CXX_STANDARD 23)
#set(CMAKE_CXX_COMPILER /usr/bin/g++)
# -rdynamic
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lpqxx -lpq -rdynamic")


add_executable(statparser
        src/main.cpp
        src/log_stream.cpp
        src/variables.h
        src/usings.h
        src/sql.cpp
        src/ssl.cpp
        src/response.cpp
        src/include.h
        src/collector.cpp
)

target_link_libraries(statparser pqxx)
find_package(ZLIB)
target_link_libraries(statparser ZLIB::ZLIB)

set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.36.0 COMPONENTS iostreams)
include_directories(${Boost_INCLUDE_DIRS})
target_link_libraries(statparser ${Boost_LIBRARIES})

find_package(nlohmann_json)
target_link_libraries(statparser nlohmann_json::nlohmann_json)

find_package(OpenSSL REQUIRED)
target_link_libraries(statparser OpenSSL::SSL)

include_directories(/usr/include/mono-2.0)
target_link_libraries(statparser mono-2.0)

find_package(OpenSSL REQUIRED)

target_link_libraries(statparser curl)

find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})
target_link_libraries(statparser ${PYTHON_LIBRARIES})

#target_link_libraries(YourExecutable ${LUAJIT_LIBRARY})