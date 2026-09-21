# Full solution: Read Pointer Relationships

This worked implementation demonstrates address, dereference, pointer arithmetic. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Read Pointer Relationships */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool checked_sum(const int32_t *values, size_t count, int64_t *out_sum) {
    if (out_sum == NULL || (values == NULL && count != 0U)) return false;
    if (count > SIZE_MAX / sizeof *values) return false;
    int64_t sum = 0; for (size_t index = 0U; index < count; ++index) sum += values[index];
    *out_sum = sum; return true;
}
```
