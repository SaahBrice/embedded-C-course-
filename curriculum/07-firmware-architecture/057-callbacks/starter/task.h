#ifndef LEARN_CALLBACKS_TASK_H
#define LEARN_CALLBACKS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef bool (*status_callback)(void *context, uint8_t value);
bool callback_run_once(status_callback callback, void *context, uint8_t value);

#endif
