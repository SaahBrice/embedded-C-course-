# Full solution: Prevent Lifetime Defects

This worked implementation demonstrates automatic storage, static storage, dangling pointers. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Prevent Lifetime Defects */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool snapshot_i16(const int16_t *source, int16_t *destination) { if (source==NULL||destination==NULL) return false; *destination=*source; return true; }
```
