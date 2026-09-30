#ifndef LEARN_CONST_AND_VOLATILE_TASK_H
#define LEARN_CONST_AND_VOLATILE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool sample_volatile_register(volatile const uint32_t *reg, uint32_t *out_value);

#endif
