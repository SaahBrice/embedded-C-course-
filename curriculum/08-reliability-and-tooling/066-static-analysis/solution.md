# Full solution: Act on Static Analysis

This worked implementation demonstrates data flow, false positive, warning policy. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Act on Static Analysis */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool checked_array_read(const int32_t *values,size_t count,size_t index,int32_t *out_value){if(values==NULL||out_value==NULL||index>=count)return false;*out_value=values[index];return true;}
```
