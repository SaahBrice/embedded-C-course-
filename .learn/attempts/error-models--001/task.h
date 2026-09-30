#ifndef LEARN_ERROR_MODELS_TASK_H
#define LEARN_ERROR_MODELS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum scale_status { SCALE_OK, SCALE_ARGUMENT, SCALE_RANGE };
enum scale_status sensor_scale(uint16_t raw, uint16_t maximum_raw, int32_t *out_milli);

#endif
