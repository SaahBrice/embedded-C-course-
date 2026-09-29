#ifndef LEARN_ALIGNMENT_ENDIANNESS_TASK_H
#define LEARN_ALIGNMENT_ENDIANNESS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool decode_u32_be(const uint8_t *bytes, size_t length, uint32_t *out_value);

#endif
