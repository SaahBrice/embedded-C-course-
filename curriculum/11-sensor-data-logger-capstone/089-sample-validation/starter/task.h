#ifndef LEARN_SAMPLE_VALIDATION_TASK_H
#define LEARN_SAMPLE_VALIDATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct sensor_sample { int32_t temperature_milli_c; uint16_t humidity_centi_percent; };
bool sample_valid(const struct sensor_sample *sample);

#endif
