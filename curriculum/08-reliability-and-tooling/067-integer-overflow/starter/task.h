#ifndef LEARN_INTEGER_OVERFLOW_TASK_H
#define LEARN_INTEGER_OVERFLOW_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool checked_scale(int32_t value, int32_t multiplier, int32_t *out_value);

#endif
