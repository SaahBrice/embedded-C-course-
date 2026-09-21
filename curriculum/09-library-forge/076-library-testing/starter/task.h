#ifndef LEARN_LIBRARY_TESTING_TASK_H
#define LEARN_LIBRARY_TESTING_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool ring_state_valid(size_t head, size_t tail, size_t count, size_t capacity);

#endif
