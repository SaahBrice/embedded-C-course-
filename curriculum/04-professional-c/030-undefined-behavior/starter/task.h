#ifndef LEARN_UNDEFINED_BEHAVIOR_TASK_H
#define LEARN_UNDEFINED_BEHAVIOR_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value);

#endif
