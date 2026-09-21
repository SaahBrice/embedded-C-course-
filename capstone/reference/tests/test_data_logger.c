#include "data_logger.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

struct fake {
    struct data_logger_sample sample;
    enum data_logger_io_result sensor_result;
    enum data_logger_io_result storage_result;
    enum data_logger_io_result transport_results[8];
    size_t transport_result_count;
    size_t transport_index;
    uint32_t now;
    unsigned storage_calls;
    unsigned transport_calls;
    uint8_t last_wire[DATA_LOGGER_WIRE_SIZE];
};

static enum data_logger_io_result sensor_read(void *context, struct data_logger_sample *sample) {
    struct fake *fake = context;
    if (fake->sensor_result == DATA_LOGGER_IO_OK) *sample = fake->sample;
    return fake->sensor_result;
}
static uint32_t clock_now(void *context) { return ((struct fake *)context)->now; }
static enum data_logger_io_result storage_write(void *context, const uint8_t *data, size_t length) {
    struct fake *fake = context;
    fake->storage_calls++;
    if (length == sizeof fake->last_wire) memcpy(fake->last_wire, data, length);
    return fake->storage_result;
}
static enum data_logger_io_result transport_send(void *context, const uint8_t *data, size_t length) {
    struct fake *fake = context;
    (void)data;
    (void)length;
    fake->transport_calls++;
    if (fake->transport_index < fake->transport_result_count) {
        return fake->transport_results[fake->transport_index++];
    }
    return DATA_LOGGER_IO_OK;
}

static void setup(struct data_logger *logger, struct fake *fake, unsigned retries) {
    memset(fake, 0, sizeof *fake);
    fake->sample = (struct data_logger_sample){21500, 3300U, 1U};
    fake->sensor_result = DATA_LOGGER_IO_OK;
    fake->storage_result = DATA_LOGGER_IO_OK;
    fake->now = 0x12345678U;
    const struct data_logger_ports ports = {
        fake, sensor_read, fake, clock_now, fake, storage_write, fake, transport_send
    };
    const struct data_logger_config config = {-40000, 125000, 3300U, retries};
    assert(data_logger_init(logger, &ports, &config) == DATA_LOGGER_OK);
}

static void test_init(void) {
    struct data_logger logger;
    struct fake fake;
    setup(&logger, &fake, 2U);
    assert(data_logger_pending(&logger) == 0U);
    assert(strcmp(data_logger_version(), "1.0.0") == 0);
    assert(data_logger_init(NULL, NULL, NULL) == DATA_LOGGER_ARGUMENT);
}

static void test_validation_is_atomic(void) {
    struct data_logger logger;
    struct fake fake;
    setup(&logger, &fake, 2U);
    fake.sample.milli_celsius = 125001;
    assert(data_logger_acquire(&logger) == DATA_LOGGER_SAMPLE_RANGE);
    assert(data_logger_pending(&logger) == 0U && logger.next_sequence == 0U);
    fake.sample.milli_celsius = 20000;
    assert(data_logger_acquire(&logger) == DATA_LOGGER_OK);
    assert(data_logger_pending(&logger) == 1U && logger.next_sequence == 1U);
}

static void test_sensor_failures(void) {
    struct data_logger logger;
    struct fake fake;
    setup(&logger, &fake, 0U);
    fake.sensor_result = DATA_LOGGER_IO_TEMPORARY;
    assert(data_logger_acquire(&logger) == DATA_LOGGER_SENSOR_TEMPORARY);
    fake.sensor_result = DATA_LOGGER_IO_PERMANENT;
    assert(data_logger_acquire(&logger) == DATA_LOGGER_SENSOR_PERMANENT);
}

static void test_full_and_wrap(void) {
    struct data_logger logger;
    struct fake fake;
    setup(&logger, &fake, 0U);
    for (size_t index = 0U; index < DATA_LOGGER_CAPACITY; ++index) {
        fake.sample.milli_celsius = (int32_t)index;
        assert(data_logger_acquire(&logger) == DATA_LOGGER_OK);
    }
    assert(data_logger_acquire(&logger) == DATA_LOGGER_FULL);
    assert(data_logger_flush_one(&logger) == DATA_LOGGER_OK);
    assert(data_logger_acquire(&logger) == DATA_LOGGER_OK);
    assert(data_logger_pending(&logger) == DATA_LOGGER_CAPACITY);
}

static void test_serialization(void) {
    const struct data_logger_record record = {0x01020304U, 0xA0B0C0D0U, {-1000, 3300U, 0x55AAU}};
    uint8_t wire[DATA_LOGGER_WIRE_SIZE] = {0U};
    assert(data_logger_encode(&record, wire, sizeof wire) == sizeof wire);
    const uint8_t prefix[] = {1U, 4U, 3U, 2U, 1U, 0xD0U, 0xC0U, 0xB0U, 0xA0U};
    assert(memcmp(wire, prefix, sizeof prefix) == 0);
    assert(data_logger_encode(&record, wire, sizeof wire - 1U) == 0U);
}

static void test_storage_failure_retains_record(void) {
    struct data_logger logger;
    struct fake fake;
    setup(&logger, &fake, 2U);
    assert(data_logger_acquire(&logger) == DATA_LOGGER_OK);
    fake.storage_result = DATA_LOGGER_IO_TEMPORARY;
    assert(data_logger_flush_one(&logger) == DATA_LOGGER_STORAGE_TEMPORARY);
    assert(data_logger_pending(&logger) == 1U && fake.transport_calls == 0U);
}

static void test_transport_retry_and_no_duplicate_storage(void) {
    struct data_logger logger;
    struct fake fake;
    setup(&logger, &fake, 1U);
    assert(data_logger_acquire(&logger) == DATA_LOGGER_OK);
    fake.transport_results[0] = DATA_LOGGER_IO_TEMPORARY;
    fake.transport_results[1] = DATA_LOGGER_IO_TEMPORARY;
    fake.transport_result_count = 2U;
    assert(data_logger_flush_one(&logger) == DATA_LOGGER_TRANSPORT_TEMPORARY);
    assert(fake.storage_calls == 1U && fake.transport_calls == 2U && data_logger_pending(&logger) == 1U);
    fake.transport_result_count = 0U;
    fake.transport_index = 0U;
    assert(data_logger_flush_one(&logger) == DATA_LOGGER_OK);
    assert(fake.storage_calls == 1U && data_logger_pending(&logger) == 0U);
}

int main(void) {
    test_init();
    test_validation_is_atomic();
    test_sensor_failures();
    test_full_and_wrap();
    test_serialization();
    test_storage_failure_retains_record();
    test_transport_retry_and_no_duplicate_storage();
    puts("data_logger: 7 suites passed");
    return 0;
}
