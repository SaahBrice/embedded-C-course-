# Full solution: Control Output with PWM

This worked implementation demonstrates frequency, duty cycle, timer period. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Control Output with PWM */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool pwm_compare(uint32_t period_ticks, uint8_t duty_percent, uint32_t *out_compare) {
    if (out_compare == NULL || period_ticks == 0U || duty_percent > 100U) return false;
    *out_compare = (uint32_t)(((uint64_t)period_ticks * duty_percent + 50U) / 100U);
    return true;
}
```
