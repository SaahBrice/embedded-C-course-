#ifndef LEARN_DATA_LOGGER_INTEGRATION_TASK_H
#define LEARN_DATA_LOGGER_INTEGRATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define INTEGRATED_LOGGER_CAPACITY 2U
enum logger_io { LOGGER_IO_OK, LOGGER_IO_TEMPORARY, LOGGER_IO_PERMANENT };
enum logger_result { LOGGER_OK, LOGGER_ARGUMENT, LOGGER_SENSOR_FAILURE, LOGGER_RANGE, LOGGER_FULL, LOGGER_EMPTY, LOGGER_STORAGE_FAILURE, LOGGER_TRANSPORT_FAILURE };
struct logger_ports { void *context; enum logger_io (*read)(void *, int32_t *); uint32_t (*now)(void *); enum logger_io (*store)(void *, const uint8_t *, size_t); enum logger_io (*send)(void *, const uint8_t *, size_t); };
struct logger_slot { uint32_t sequence, timestamp; int32_t value; bool persisted; };
struct integrated_logger { struct logger_ports ports; struct logger_slot slots[INTEGRATED_LOGGER_CAPACITY]; size_t head, tail, count; uint32_t next_sequence; unsigned retry_limit; };
enum logger_result logger_init(struct integrated_logger *logger, const struct logger_ports *ports, unsigned retry_limit);
enum logger_result logger_capture(struct integrated_logger *logger);
enum logger_result logger_flush_one(struct integrated_logger *logger);

#endif
