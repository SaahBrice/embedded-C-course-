#ifndef LEARN_API_DESIGN_TASK_H
#define LEARN_API_DESIGN_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool counter_add_bounded(unsigned current, unsigned increment, unsigned limit, unsigned *out_value);

#endif
