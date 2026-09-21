# Full solution: Control Expression Evaluation

This worked implementation demonstrates precedence, short circuiting, side effects. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Control Expression Evaluation */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint32_t status_bits_update(uint32_t status, uint32_t set_mask, uint32_t clear_mask) { return (status | set_mask) & ~clear_mask; }
```
