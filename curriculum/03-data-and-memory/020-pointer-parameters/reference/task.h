#ifndef LEARN_POINTER_PARAMETERS_TASK_H
#define LEARN_POINTER_PARAMETERS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool decode_u16_le(const uint8_t *bytes, size_t length, uint16_t *out_value);

#endif
