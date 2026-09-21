# Full solution: Implement Your First Firmware Function

This worked implementation demonstrates declarations, definitions, unsigned status. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Implement Your First Firmware Function */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

int firmware_status(unsigned boot_count) { return boot_count == 0U ? -1 : 0; }
```
