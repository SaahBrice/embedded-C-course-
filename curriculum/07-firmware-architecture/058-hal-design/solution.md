# Full solution: Define a Hardware Abstraction Boundary

This worked implementation demonstrates ports, adapters, portable core. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Define a Hardware Abstraction Boundary */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool controller_step(const struct controller_hal *hal, int32_t maximum) {
    if (hal == NULL || hal->read_sensor == NULL || hal->set_alarm == NULL) return false;
    int32_t value = 0;
    if (!hal->read_sensor(hal->context, &value)) { hal->set_alarm(hal->context, true); return false; }
    hal->set_alarm(hal->context, value > maximum);
    return true;
}
```
