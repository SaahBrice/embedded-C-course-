#ifndef LEARN_GDB_FIRST_STEPS_TASK_H
#define LEARN_GDB_FIRST_STEPS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool sample_sum(const int16_t *samples, size_t count, int32_t *out_sum);
bool sample_minimum(const int16_t *samples, size_t count, int16_t *out_minimum);
bool sample_negative_mask(const int16_t *samples, size_t count, uint8_t *out_mask);
bool sample_window_analyze(const int16_t *samples, size_t count, int32_t *out_sum, int16_t *out_minimum, uint8_t *out_negative_mask);

#endif
