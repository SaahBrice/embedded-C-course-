# Full solution: Route Fault States

This worked implementation demonstrates if, switch, enumerated states. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Route Fault States */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum measurement_action classify_measurement(int32_t value, bool sensor_fault) {
    if (sensor_fault) return ACTION_SHUTDOWN;
    if (value < -40000 || value > 125000) return ACTION_RETRY;
    return ACTION_ACCEPT;
}
```
