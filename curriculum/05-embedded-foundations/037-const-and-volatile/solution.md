# Full solution: Apply const and volatile Correctly

This worked implementation demonstrates read-only interfaces, observable side effects, optimization. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Apply const and volatile Correctly */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool sample_volatile_register(volatile const uint32_t *reg,uint32_t *out_value){if(reg==NULL||out_value==NULL)return false;*out_value=*reg;return true;}
```
