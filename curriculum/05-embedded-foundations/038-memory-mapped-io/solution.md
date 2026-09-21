# Full solution: Model Memory-Mapped I/O

This worked implementation demonstrates volatile access, register offsets, read-modify-write. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Model Memory-Mapped I/O */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool register_update(volatile uint32_t *reg, uint32_t clear_mask, uint32_t set_mask) {
    if (reg == NULL) return false;
    const uint32_t current = *reg;
    *reg = (current & ~clear_mask) | set_mask;
    return true;
}
```
