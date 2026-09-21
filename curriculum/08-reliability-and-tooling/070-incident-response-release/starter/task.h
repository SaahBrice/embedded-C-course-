#ifndef LEARN_INCIDENT_RESPONSE_RELEASE_TASK_H
#define LEARN_INCIDENT_RESPONSE_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

bool watchdog_elapsed(uint32_t now, uint32_t last_kick, uint32_t timeout);
bool ring_indices_valid(size_t head, size_t tail, size_t count, size_t capacity);
bool recovery_required(bool watchdog_expired, bool ring_valid, unsigned consecutive_errors, unsigned error_limit);

#endif
