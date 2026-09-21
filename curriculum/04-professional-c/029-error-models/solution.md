# Full solution: Propagate Errors Without Guessing

This worked implementation demonstrates status codes, out parameters, error context. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Propagate Errors Without Guessing */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum scale_status sensor_scale(uint16_t raw, uint16_t maximum_raw, int32_t *out_milli) {
    if (out_milli == NULL || maximum_raw == 0U) return SCALE_ARGUMENT;
    if (raw > maximum_raw) return SCALE_RANGE;
    *out_milli = (int32_t)(((uint32_t)raw * UINT32_C(1000) + maximum_raw / 2U) / maximum_raw); return SCALE_OK;
}
```
