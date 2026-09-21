#ifndef LEARN_DEFENSIVE_APIS_TASK_H
#define LEARN_DEFENSIVE_APIS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool bounded_copy(uint8_t *destination, size_t capacity, const uint8_t *source, size_t count);

#endif
