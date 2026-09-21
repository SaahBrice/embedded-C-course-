cmake_minimum_required(VERSION 3.20)
project(DataLogger VERSION 1.0.0 LANGUAGES C)

add_library(data_logger src/data_logger.c)
target_include_directories(data_logger PUBLIC include)
target_compile_features(data_logger PUBLIC c_std_11)
target_compile_options(data_logger PRIVATE -Wall -Wextra -Wpedantic -Werror)

add_executable(logger_demo examples/logger_demo.c)
target_link_libraries(logger_demo PRIVATE data_logger)
target_compile_options(logger_demo PRIVATE -Wall -Wextra -Wpedantic -Werror)

enable_testing()
add_executable(data_logger_tests tests/test_data_logger.c)
target_link_libraries(data_logger_tests PRIVATE data_logger)
target_compile_options(data_logger_tests PRIVATE -Wall -Wextra -Wpedantic -Werror)
add_test(NAME data_logger_tests COMMAND data_logger_tests)
