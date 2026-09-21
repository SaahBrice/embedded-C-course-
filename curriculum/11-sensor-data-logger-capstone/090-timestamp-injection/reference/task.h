#ifndef LEARN_TIMESTAMP_INJECTION_TASK_H
#define LEARN_TIMESTAMP_INJECTION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef uint32_t (*clock_now_fn)(void *context);
struct timestamped_value { uint32_t timestamp_ms; int32_t value; };
bool timestamp_record(clock_now_fn now, void *context, int32_t value, struct timestamped_value *out_record);

#endif
