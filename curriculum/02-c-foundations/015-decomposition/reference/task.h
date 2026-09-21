#ifndef LEARN_DECOMPOSITION_TASK_H
#define LEARN_DECOMPOSITION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool scale_offset_sample(int32_t raw, int32_t offset, int32_t scale, int32_t *out_value);

#endif
