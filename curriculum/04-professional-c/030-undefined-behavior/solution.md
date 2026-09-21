# Full solution: Recognize Undefined Behavior

This worked implementation demonstrates overflow, invalid shifts, aliasing, sequence rules. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Recognize Undefined Behavior */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool safe_left_shift(uint32_t value, unsigned shift, uint32_t *out_value) {
    if (out_value == NULL || shift >= 32U || value > (UINT32_MAX >> shift)) return false;
    *out_value = value << shift; return true;
}
```
