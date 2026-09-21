cmake_minimum_required(VERSION 3.20)
project(RecordQueue VERSION 1.0.0 LANGUAGES C)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

add_library(record_queue src/record_queue.c)
add_library(Learn::record_queue ALIAS record_queue)
target_compile_features(record_queue PUBLIC c_std_11)
target_compile_options(record_queue PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_include_directories(record_queue
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

enable_testing()
add_executable(record_queue_tests tests/test_record_queue.c)
target_link_libraries(record_queue_tests PRIVATE record_queue)
target_compile_options(record_queue_tests PRIVATE -Wall -Wextra -Wpedantic -Werror)
add_test(NAME record_queue_tests COMMAND record_queue_tests)

configure_package_config_file(
    cmake/RecordQueueConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/RecordQueueConfig.cmake
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/RecordQueue
)
write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/RecordQueueConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)
install(TARGETS record_queue EXPORT RecordQueueTargets ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(EXPORT RecordQueueTargets NAMESPACE Learn:: DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/RecordQueue)
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/RecordQueueConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/RecordQueueConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/RecordQueue
)
