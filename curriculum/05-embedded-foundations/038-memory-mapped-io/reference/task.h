#ifndef LEARN_MEMORY_MAPPED_IO_TASK_H
#define LEARN_MEMORY_MAPPED_IO_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool register_update(volatile uint32_t *reg, uint32_t clear_mask, uint32_t set_mask);

#endif
