#include "task.h"

/* TODO — Route Fault States: implement the declared interface.
 * Contract to prove: Fault status has priority; otherwise the inclusive sensor range is accepted and out-of-range data is retried.
 */
enum measurement_action classify_measurement(int32_t value, bool sensor_fault) {
    if (sensor_fault) return ACTION_SHUTDOWN;
    if (value < -40000 || value > 125000) return ACTION_RETRY;
    return ACTION_ACCEPT;
}