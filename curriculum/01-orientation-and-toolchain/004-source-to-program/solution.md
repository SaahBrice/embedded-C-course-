# Full solution: Trace Source to Executable

This worked implementation demonstrates preprocessing, compilation, assembly, linking. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Trace Source to Executable */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool linked_increment(int32_t input, int32_t *out_value) {
    if (out_value == NULL || input == INT32_MAX) return false;
    *out_value = input + 1; return true;
}
```
