#ifndef LEARN_TELEMETRY_CLI_RELEASE_TASK_H
#define LEARN_TELEMETRY_CLI_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
#include <math.h>

bool celsius_in_sensor_range(double celsius);
bool celsius_to_milli(double celsius, int32_t *out_milli_celsius);
bool telemetry_prepare(double celsius, bool sensor_fault, int32_t *out_milli_celsius);

#endif
