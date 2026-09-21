#ifndef LEARN_CONFIGURATION_TASK_H
#define LEARN_CONFIGURATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool controller_config_valid(uint32_t sample_period_ms, int32_t low_limit, int32_t high_limit);

#endif
