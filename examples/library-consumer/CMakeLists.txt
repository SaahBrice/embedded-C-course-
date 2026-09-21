cmake_minimum_required(VERSION 3.20)
project(RecordQueueConsumer LANGUAGES C)

find_package(RecordQueue 1 CONFIG REQUIRED)
add_executable(record_queue_consumer main.c)
target_compile_features(record_queue_consumer PRIVATE c_std_11)
target_compile_options(record_queue_consumer PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(record_queue_consumer PRIVATE Learn::record_queue)
