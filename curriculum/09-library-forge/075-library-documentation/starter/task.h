#ifndef LEARN_LIBRARY_DOCUMENTATION_TASK_H
#define LEARN_LIBRARY_DOCUMENTATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool documented_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count);

#endif
