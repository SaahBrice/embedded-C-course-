#ifndef LEARN_INTEGRATION_TESTING_TASK_H
#define LEARN_INTEGRATION_TESTING_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct logger_ports { void *context; bool (*read)(void *, int32_t *); bool (*store)(void *, int32_t); };
bool logger_cycle(const struct logger_ports *ports);

#endif
