#ifndef LEARN_HAL_DESIGN_TASK_H
#define LEARN_HAL_DESIGN_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct controller_hal { void *context; bool (*read_sensor)(void *, int32_t *); void (*set_alarm)(void *, bool); };
bool controller_step(const struct controller_hal *hal, int32_t maximum);

#endif
