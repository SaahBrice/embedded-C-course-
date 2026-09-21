#ifndef LEARN_CONTROLLER_RELEASE_TASK_H
#define LEARN_CONTROLLER_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct sensor_controller { uint32_t period; uint32_t last_sample; unsigned samples; };
bool sensor_controller_due(const struct sensor_controller *controller, uint32_t now);
bool sensor_sample_acceptable(bool sensor_ready, int32_t value, int32_t minimum, int32_t maximum);
bool sensor_controller_update(struct sensor_controller *controller, uint32_t now, bool sensor_ready);

#endif
