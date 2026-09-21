# Full solution: Decompose a Firmware Ticket

This worked implementation demonstrates contracts, cohesion, coupling. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Decompose a Firmware Ticket */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool scale_offset_sample(int32_t raw, int32_t offset, int32_t scale, int32_t *out_value) {
    if (out_value == NULL) return false;
    const int64_t value=((int64_t)raw+offset)*scale;
    if (value<INT32_MIN || value>INT32_MAX) return false;
    *out_value=(int32_t)value; return true;
}
```
