#ifndef LEARN_STATE_MACHINES_TASK_H
#define LEARN_STATE_MACHINES_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum controller_state { CONTROLLER_IDLE, CONTROLLER_SAMPLING, CONTROLLER_FAULT };
enum controller_event { EVENT_START, EVENT_SAMPLE_OK, EVENT_SAMPLE_BAD, EVENT_RESET };
enum controller_state controller_transition(enum controller_state state, enum controller_event event);

#endif
