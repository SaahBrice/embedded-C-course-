#ifndef LEARN_CPU_MEMORY_MODEL_TASK_H
#define LEARN_CPU_MEMORY_MODEL_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

uint32_t load_modify_value(uint32_t loaded, uint32_t set_mask, uint32_t clear_mask);

#endif
