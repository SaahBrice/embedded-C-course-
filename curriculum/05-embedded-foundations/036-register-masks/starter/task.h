#ifndef LEARN_REGISTER_MASKS_TASK_H
#define LEARN_REGISTER_MASKS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool register_field_write(uint32_t original, uint32_t mask, unsigned shift, uint32_t field_value, uint32_t *out_value);

#endif
