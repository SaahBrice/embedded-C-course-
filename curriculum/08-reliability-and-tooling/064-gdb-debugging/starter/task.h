#ifndef LEARN_GDB_DEBUGGING_TASK_H
#define LEARN_GDB_DEBUGGING_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

size_t replace_value(int32_t *values, size_t count, int32_t target, int32_t replacement);

#endif
