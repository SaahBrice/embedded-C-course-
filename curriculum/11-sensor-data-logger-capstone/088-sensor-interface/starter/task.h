#ifndef LEARN_SENSOR_INTERFACE_TASK_H
#define LEARN_SENSOR_INTERFACE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum sensor_status { SENSOR_OK, SENSOR_UNAVAILABLE, SENSOR_RANGE };
typedef enum sensor_status (*sensor_read_fn)(void *context, int32_t *out_value);
enum sensor_status sensor_read_checked(sensor_read_fn read, void *context, int32_t minimum, int32_t maximum, int32_t *out_value);

#endif
