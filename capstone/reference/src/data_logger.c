#include "data_logger.h"

#include <string.h>

static int ports_valid(const struct data_logger_ports *ports) {
    return ports != NULL && ports->sensor_read != NULL && ports->clock_now != NULL &&
           ports->storage_write != NULL && ports->transport_send != NULL;
}

static int config_valid(const struct data_logger_config *config) {
    return config != NULL && config->minimum_milli_celsius <= config->maximum_milli_celsius &&
           config->maximum_millivolts > 0U && config->transport_retry_limit <= 10U;
}

enum data_logger_status data_logger_init(
    struct data_logger *logger,
    const struct data_logger_ports *ports,
    const struct data_logger_config *config
) {
    if (logger == NULL || !ports_valid(ports) || !config_valid(config)) return DATA_LOGGER_ARGUMENT;
    memset(logger, 0, sizeof *logger);
    logger->ports = *ports;
    logger->config = *config;
    return DATA_LOGGER_OK;
}

static int sample_valid(const struct data_logger *logger, const struct data_logger_sample *sample) {
    return sample->milli_celsius >= logger->config.minimum_milli_celsius &&
           sample->milli_celsius <= logger->config.maximum_milli_celsius &&
           sample->millivolts <= logger->config.maximum_millivolts;
}

enum data_logger_status data_logger_acquire(struct data_logger *logger) {
    if (logger == NULL) return DATA_LOGGER_ARGUMENT;
    if (logger->count == DATA_LOGGER_CAPACITY) return DATA_LOGGER_FULL;
    struct data_logger_sample sample;
    const enum data_logger_io_result read = logger->ports.sensor_read(logger->ports.sensor_context, &sample);
    if (read == DATA_LOGGER_IO_TEMPORARY) return DATA_LOGGER_SENSOR_TEMPORARY;
    if (read != DATA_LOGGER_IO_OK) return DATA_LOGGER_SENSOR_PERMANENT;
    if (!sample_valid(logger, &sample)) return DATA_LOGGER_SAMPLE_RANGE;

    struct data_logger_slot *slot = &logger->slots[logger->head];
    slot->record.sequence = logger->next_sequence;
    slot->record.timestamp_ms = logger->ports.clock_now(logger->ports.clock_context);
    slot->record.sample = sample;
    slot->persisted = 0;
    logger->head = (logger->head + 1U) % DATA_LOGGER_CAPACITY;
    logger->count++;
    logger->next_sequence++;
    return DATA_LOGGER_OK;
}

static void put_u16(uint8_t *destination, uint16_t value) {
    destination[0] = (uint8_t)value;
    destination[1] = (uint8_t)(value >> 8U);
}

static void put_u32(uint8_t *destination, uint32_t value) {
    destination[0] = (uint8_t)value;
    destination[1] = (uint8_t)(value >> 8U);
    destination[2] = (uint8_t)(value >> 16U);
    destination[3] = (uint8_t)(value >> 24U);
}

size_t data_logger_encode(
    const struct data_logger_record *record,
    uint8_t *destination,
    size_t capacity
) {
    if (record == NULL || destination == NULL || capacity < DATA_LOGGER_WIRE_SIZE) return 0U;
    destination[0] = DATA_LOGGER_FORMAT_VERSION;
    put_u32(destination + 1U, record->sequence);
    put_u32(destination + 5U, record->timestamp_ms);
    put_u32(destination + 9U, (uint32_t)record->sample.milli_celsius);
    put_u16(destination + 13U, record->sample.millivolts);
    put_u16(destination + 15U, record->sample.quality_flags);
    uint8_t checksum = 0U;
    for (size_t index = 0U; index < DATA_LOGGER_WIRE_SIZE - 1U; ++index) checksum ^= destination[index];
    destination[DATA_LOGGER_WIRE_SIZE - 1U] = checksum;
    return DATA_LOGGER_WIRE_SIZE;
}

static enum data_logger_status storage_status(enum data_logger_io_result result) {
    return result == DATA_LOGGER_IO_TEMPORARY ? DATA_LOGGER_STORAGE_TEMPORARY : DATA_LOGGER_STORAGE_PERMANENT;
}

enum data_logger_status data_logger_flush_one(struct data_logger *logger) {
    if (logger == NULL) return DATA_LOGGER_ARGUMENT;
    if (logger->count == 0U) return DATA_LOGGER_EMPTY;
    struct data_logger_slot *slot = &logger->slots[logger->tail];
    uint8_t wire[DATA_LOGGER_WIRE_SIZE];
    if (data_logger_encode(&slot->record, wire, sizeof wire) != sizeof wire) return DATA_LOGGER_ARGUMENT;
    if (!slot->persisted) {
        const enum data_logger_io_result stored = logger->ports.storage_write(
            logger->ports.storage_context, wire, sizeof wire
        );
        if (stored != DATA_LOGGER_IO_OK) return storage_status(stored);
        slot->persisted = 1;
    }
    for (unsigned attempt = 0U; attempt <= logger->config.transport_retry_limit; ++attempt) {
        const enum data_logger_io_result sent = logger->ports.transport_send(
            logger->ports.transport_context, wire, sizeof wire
        );
        if (sent == DATA_LOGGER_IO_OK) {
            logger->tail = (logger->tail + 1U) % DATA_LOGGER_CAPACITY;
            logger->count--;
            return DATA_LOGGER_OK;
        }
        if (sent == DATA_LOGGER_IO_PERMANENT) return DATA_LOGGER_TRANSPORT_PERMANENT;
    }
    return DATA_LOGGER_TRANSPORT_TEMPORARY;
}

size_t data_logger_pending(const struct data_logger *logger) { return logger == NULL ? 0U : logger->count; }
const char *data_logger_version(void) { return "1.0.0"; }
