#ifndef LEARN_PORTABILITY_TASK_H
#define LEARN_PORTABILITY_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool read_u32_le(const uint8_t *bytes, size_t length, uint32_t *out_value);

#endif
