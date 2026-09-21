#ifndef LEARN_TIMERS_TASK_H
#define LEARN_TIMERS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool deadline_reached(uint32_t now, uint32_t deadline);

#endif
