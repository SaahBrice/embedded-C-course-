# Full solution: Harden Arithmetic

This worked implementation demonstrates checked operations, saturation, conversion. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Harden Arithmetic */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool checked_scale(int32_t value, int32_t multiplier, int32_t *out_value) {
    if (out_value == NULL) return false;
    const int64_t wide=(int64_t)value*multiplier;
    if(wide<INT32_MIN||wide>INT32_MAX)return false;
    *out_value=(int32_t)wide;
    return true;
}
```
