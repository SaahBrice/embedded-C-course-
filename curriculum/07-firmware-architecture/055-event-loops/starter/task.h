#ifndef LEARN_EVENT_LOOPS_TASK_H
#define LEARN_EVENT_LOOPS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool task_due(uint32_t now, uint32_t last_run, uint32_t period);

#endif
