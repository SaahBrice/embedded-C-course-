# Full solution: Process a Sample Window

This worked implementation demonstrates for, while, loop invariants. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Process a Sample Window */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool sample_average(const int16_t *samples, size_t count, int32_t *out_average) {
    if (samples == NULL || out_average == NULL || count == 0U) return false;
    int64_t total = 0; for (size_t i = 0U; i < count; ++i) total += samples[i];
    *out_average = (int32_t)(total / (int64_t)count); return true;
}
```
