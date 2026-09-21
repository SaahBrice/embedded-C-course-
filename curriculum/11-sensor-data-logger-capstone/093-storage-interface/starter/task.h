#ifndef LEARN_STORAGE_INTERFACE_TASK_H
#define LEARN_STORAGE_INTERFACE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef size_t (*storage_write_fn)(void *context, const uint8_t *bytes, size_t length);
bool storage_write_all(storage_write_fn write, void *context, const uint8_t *bytes, size_t length);

#endif
