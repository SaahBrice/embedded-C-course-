# Full solution: Implement a Tiny Scheduler

This worked implementation demonstrates period, deadline, wraparound. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Implement a Tiny Scheduler */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool scheduler_release(struct scheduled_task *task,uint32_t now){if(task==NULL||task->period==0U||(int32_t)(now-task->next_release)<0)return false;task->next_release+=task->period;++task->runs;return true;}
```
