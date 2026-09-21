# Full solution: Use Fixed-Width Integers

This worked implementation demonstrates stdint, UINT32_C, format macros. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Use Fixed-Width Integers */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint32_t saturating_counter_add(uint32_t counter, uint32_t increment) { return increment > UINT32_MAX - counter ? UINT32_MAX : counter + increment; }
```
