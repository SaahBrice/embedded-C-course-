#ifndef LEARN_COOPERATIVE_SCHEDULER_TASK_H
#define LEARN_COOPERATIVE_SCHEDULER_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct scheduled_task { uint32_t period; uint32_t next_release; unsigned runs; };
bool scheduler_release(struct scheduled_task *task, uint32_t now);

#endif
