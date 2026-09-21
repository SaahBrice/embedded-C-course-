#ifndef LEARN_STATIC_ANALYSIS_TASK_H
#define LEARN_STATIC_ANALYSIS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool checked_array_read(const int32_t *values, size_t count, size_t index, int32_t *out_value);

#endif
