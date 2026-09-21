#include "data_logger.h"

#include <stdio.h>

struct demo_context { unsigned sample_index, stored, transported; uint32_t now; };

static enum data_logger_io_result read_sensor(void *context, struct data_logger_sample *sample) {
    struct demo_context *demo = context;
    sample->milli_celsius = 20000 + (int32_t)(demo->sample_index * 250U);
    sample->millivolts = 3300U;
    sample->quality_flags = 1U;
    demo->sample_index++;
    return DATA_LOGGER_IO_OK;
}
static uint32_t read_clock(void *context) { struct demo_context *demo = context; demo->now += 1000U; return demo->now; }
static enum data_logger_io_result store(void *context, const uint8_t *data, size_t length) {
    struct demo_context *demo = context; (void)data; (void)length; demo->stored++; return DATA_LOGGER_IO_OK;
}
static enum data_logger_io_result transport(void *context, const uint8_t *data, size_t length) {
    struct demo_context *demo = context; (void)data; (void)length; demo->transported++; return DATA_LOGGER_IO_OK;
}

int main(void) {
    struct demo_context demo = {0U, 0U, 0U, 0U};
    struct data_logger logger;
    const struct data_logger_ports ports = {&demo, read_sensor, &demo, read_clock, &demo, store, &demo, transport};
    const struct data_logger_config config = {-40000, 125000, 3300U, 2U};
    if (data_logger_init(&logger, &ports, &config) != DATA_LOGGER_OK) return 1;
    for (unsigned index = 0U; index < 3U; ++index) {
        if (data_logger_acquire(&logger) != DATA_LOGGER_OK) return 1;
    }
    while (data_logger_pending(&logger) != 0U) {
        if (data_logger_flush_one(&logger) != DATA_LOGGER_OK) return 1;
    }
    printf("stored=%u transported=%u pending=%zu\n", demo.stored, demo.transported, data_logger_pending(&logger));
    return 0;
}
