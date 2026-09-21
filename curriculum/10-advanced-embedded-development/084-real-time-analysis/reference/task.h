#ifndef LEARN_REAL_TIME_ANALYSIS_TASK_H
#define LEARN_REAL_TIME_ANALYSIS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool nonpreemptive_deadline_met(uint32_t wcet_us, uint32_t blocking_us, uint32_t period_us);

#endif
