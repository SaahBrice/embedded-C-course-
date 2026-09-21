# Full solution: Choose When to Use an RTOS

This worked implementation demonstrates task, queue, mutex, priority inversion. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Choose When to Use an RTOS */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool startup_services_ready(bool memory,bool drivers,bool scheduler){return memory&&drivers&&scheduler;}
bool queue_absorbs_burst(size_t produced,size_t consumed,size_t capacity){return produced<=consumed||produced-consumed<=capacity;}
bool periodic_load_fits(uint32_t execution,uint32_t blocking,uint32_t period){return execution<=period&&blocking<=period-execution;}
bool rtos_partition_justified(unsigned jobs,bool blocking_io,bool cooperative_ok){return jobs>=2U&&(blocking_io||!cooperative_ok);}
```
