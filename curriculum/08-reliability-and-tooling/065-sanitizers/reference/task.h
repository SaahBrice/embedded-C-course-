#ifndef LEARN_SANITIZERS_TASK_H
#define LEARN_SANITIZERS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count);

#endif
