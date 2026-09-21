# Full solution: Reason About Scope and Storage

This worked implementation demonstrates block scope, file scope, static storage. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Reason About Scope and Storage */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool instance_increment(unsigned *state) { if (state == NULL || *state == UINT_MAX) return false; ++*state; return true; }
```
