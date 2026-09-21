#ifndef LEARN_CONCURRENCY_TASK_H
#define LEARN_CONCURRENCY_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool sequence_is_newer(uint32_t candidate, uint32_t current);

#endif
