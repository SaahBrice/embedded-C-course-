# Full solution: Map CPU and Memory Responsibilities

This worked implementation demonstrates registers, address space, load/store. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Map CPU and Memory Responsibilities */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint32_t load_modify_value(uint32_t loaded,uint32_t set_mask,uint32_t clear_mask){return (loaded&~clear_mask)|set_mask;}
```
