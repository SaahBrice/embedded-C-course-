# Full solution: Schedule with Hardware Timers

This worked implementation demonstrates tick, compare, overflow. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Schedule with Hardware Timers */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool deadline_reached(uint32_t now, uint32_t deadline) { return (int32_t)(now - deadline) >= 0; }
```
