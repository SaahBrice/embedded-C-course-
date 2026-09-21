#ifndef LEARN_RTOS_CONCEPTS_TASK_H
#define LEARN_RTOS_CONCEPTS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool startup_services_ready(bool memory_ready, bool drivers_ready, bool scheduler_ready);
bool queue_absorbs_burst(size_t producer_burst, size_t consumer_progress, size_t queue_capacity);
bool periodic_load_fits(uint32_t execution_us, uint32_t blocking_us, uint32_t period_us);
bool rtos_partition_justified(unsigned independent_jobs, bool shared_blocking_io, bool cooperative_deadlines_met);

#endif
