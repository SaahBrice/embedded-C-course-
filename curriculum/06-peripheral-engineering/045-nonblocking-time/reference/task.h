#ifndef LEARN_NONBLOCKING_TIME_TASK_H
#define LEARN_NONBLOCKING_TIME_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct blinker { uint32_t last_change; uint32_t period; bool level; };
bool blinker_update(struct blinker *blinker, uint32_t now);

#endif
