# Full solution: Diagnose a Firmware Fault with GDB

This worked implementation demonstrates backtrace, watchpoint, memory examine. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Diagnose a Firmware Fault with GDB */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

size_t replace_value(int32_t *values, size_t count, int32_t target, int32_t replacement) {
    if (values == NULL) return 0U;
    size_t changed=0U;
    for(size_t i=0U;i<count;++i) if(values[i]==target){values[i]=replacement;++changed;}
    return changed;
}
```
