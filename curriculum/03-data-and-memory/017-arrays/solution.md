# Full solution: Work Safely with Arrays

This worked implementation demonstrates bounds, element count, iteration. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Work Safely with Arrays */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool sample_minmax(const int16_t *samples, size_t count, int16_t *out_min, int16_t *out_max) {
    if (samples == NULL || count == 0U || out_min == NULL || out_max == NULL) return false;
    int16_t low = samples[0], high = samples[0];
    for (size_t i = 1U; i < count; ++i) { if (samples[i] < low) low = samples[i]; if (samples[i] > high) high = samples[i]; }
    *out_min = low; *out_max = high; return true;
}
```
