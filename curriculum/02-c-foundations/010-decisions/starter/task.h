#ifndef LEARN_DECISIONS_TASK_H
#define LEARN_DECISIONS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum measurement_action { ACTION_ACCEPT, ACTION_RETRY, ACTION_SHUTDOWN };
enum measurement_action classify_measurement(int32_t value, bool sensor_fault);

#endif
