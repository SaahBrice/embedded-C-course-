# Full solution: Measure Floating-Point Trade-offs

This worked implementation demonstrates representation, rounding, fixed point. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Measure Floating-Point Trade-offs */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool volts_to_millivolts(double volts, uint32_t *out_millivolts) {
    if (out_millivolts == NULL || volts < 0.0 || volts > 65.535) return false;
    *out_millivolts = (uint32_t)(volts * 1000.0 + 0.5); return true;
}
```
