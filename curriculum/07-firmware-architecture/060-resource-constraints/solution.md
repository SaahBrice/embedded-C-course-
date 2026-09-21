# Full solution: Budget Firmware Resources

This worked implementation demonstrates RAM, flash, stack, time. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Budget Firmware Resources */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool queue_storage_size(size_t capacity,size_t item_size,size_t *out_bytes){if(out_bytes==NULL||(item_size!=0U&&capacity>SIZE_MAX/item_size))return false;*out_bytes=capacity*item_size;return true;}
```
