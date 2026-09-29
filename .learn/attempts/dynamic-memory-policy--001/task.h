#ifndef LEARN_DYNAMIC_MEMORY_POLICY_TASK_H
#define LEARN_DYNAMIC_MEMORY_POLICY_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool fixed_pool_acquire(bool *used, size_t capacity, size_t *out_index);

#endif
