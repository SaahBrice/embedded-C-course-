# Full solution: Extract Testable Functions

This worked implementation demonstrates parameters, return values, single responsibility. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Extract Testable Functions */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

int32_t clamp_i32(int32_t value, int32_t minimum, int32_t maximum) {
    if (minimum > maximum) return minimum;
    if (value < minimum) return minimum;
    if (value > maximum) return maximum;
    return value;
}
```
