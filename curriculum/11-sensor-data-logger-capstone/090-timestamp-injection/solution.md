# Full solution: Capstone: Inject Time

This worked implementation demonstrates clock port, monotonic time, test determinism. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Capstone: Inject Time */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool timestamp_record(clock_now_fn now,void *context,int32_t value,struct timestamped_value *out_record){if(now==NULL||out_record==NULL)return false;struct timestamped_value record={now(context),value};*out_record=record;return true;}
```
