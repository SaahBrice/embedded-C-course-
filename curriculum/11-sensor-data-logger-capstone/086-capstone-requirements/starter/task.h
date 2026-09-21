#ifndef LEARN_CAPSTONE_REQUIREMENTS_TASK_H
#define LEARN_CAPSTONE_REQUIREMENTS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool logger_requirements_valid(uint32_t period_ms, uint32_t jitter_ms, size_t record_capacity);

#endif
