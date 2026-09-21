#ifndef DATA_LOGGER_H
#define DATA_LOGGER_H

#include <stddef.h>
#include <stdint.h>

#define DATA_LOGGER_CAPACITY 8U
#define DATA_LOGGER_WIRE_SIZE 18U
#define DATA_LOGGER_FORMAT_VERSION 1U

struct data_logger_sample {
    int32_t milli_celsius;
    uint16_t millivolts;
    uint16_t quality_flags;
};

struct data_logger_record {
    uint32_t sequence;
    uint32_t timestamp_ms;
    struct data_logger_sample sample;
};

enum data_logger_io_result {
    DATA_LOGGER_IO_OK = 0,
    DATA_LOGGER_IO_TEMPORARY,
    DATA_LOGGER_IO_PERMANENT
};

struct data_logger_ports {
    void *sensor_context;
    enum data_logger_io_result (*sensor_read)(void *context, struct data_logger_sample *sample);
    void *clock_context;
    uint32_t (*clock_now)(void *context);
    void *storage_context;
    enum data_logger_io_result (*storage_write)(void *context, const uint8_t *data, size_t length);
    void *transport_context;
    enum data_logger_io_result (*transport_send)(void *context, const uint8_t *data, size_t length);
};

struct data_logger_config {
    int32_t minimum_milli_celsius;
    int32_t maximum_milli_celsius;
    uint16_t maximum_millivolts;
    unsigned transport_retry_limit;
};

enum data_logger_status {
    DATA_LOGGER_OK = 0,
    DATA_LOGGER_ARGUMENT,
    DATA_LOGGER_SENSOR_TEMPORARY,
    DATA_LOGGER_SENSOR_PERMANENT,
    DATA_LOGGER_SAMPLE_RANGE,
    DATA_LOGGER_FULL,
    DATA_LOGGER_EMPTY,
    DATA_LOGGER_STORAGE_TEMPORARY,
    DATA_LOGGER_STORAGE_PERMANENT,
    DATA_LOGGER_TRANSPORT_TEMPORARY,
    DATA_LOGGER_TRANSPORT_PERMANENT
};

struct data_logger_slot {
    struct data_logger_record record;
    int persisted;
};

struct data_logger {
    struct data_logger_ports ports;
    struct data_logger_config config;
    struct data_logger_slot slots[DATA_LOGGER_CAPACITY];
    size_t head;
    size_t tail;
    size_t count;
    uint32_t next_sequence;
};

enum data_logger_status data_logger_init(
    struct data_logger *logger,
    const struct data_logger_ports *ports,
    const struct data_logger_config *config
);
enum data_logger_status data_logger_acquire(struct data_logger *logger);
enum data_logger_status data_logger_flush_one(struct data_logger *logger);
size_t data_logger_pending(const struct data_logger *logger);
size_t data_logger_encode(
    const struct data_logger_record *record,
    uint8_t *destination,
    size_t capacity
);
const char *data_logger_version(void);

#endif
