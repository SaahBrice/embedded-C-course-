# Full solution: Dispatch with Function Pointers

This worked implementation demonstrates callback signatures, tables, null callbacks. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Dispatch with Function Pointers */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool event_dispatch(uint8_t event, event_handler const *handlers, size_t count, void *context, uint8_t value) {
    if (handlers == NULL || event >= count || handlers[event] == NULL) return false;
    return handlers[event](context, value);
}
```
