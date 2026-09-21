#ifndef LEARN_LIBRARY_CONFIGURATION_TASK_H
#define LEARN_LIBRARY_CONFIGURATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool queue_config_valid(size_t capacity, bool overwrite_oldest);

#endif
