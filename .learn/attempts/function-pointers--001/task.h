#ifndef LEARN_FUNCTION_POINTERS_TASK_H
#define LEARN_FUNCTION_POINTERS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef bool (*event_handler)(void *context, uint8_t value);
bool event_dispatch(uint8_t event, event_handler const *handlers, size_t count, void *context, uint8_t value);

#endif
