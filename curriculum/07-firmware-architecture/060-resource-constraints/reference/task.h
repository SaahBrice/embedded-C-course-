#ifndef LEARN_RESOURCE_CONSTRAINTS_TASK_H
#define LEARN_RESOURCE_CONSTRAINTS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool queue_storage_size(size_t capacity, size_t item_size, size_t *out_bytes);

#endif
