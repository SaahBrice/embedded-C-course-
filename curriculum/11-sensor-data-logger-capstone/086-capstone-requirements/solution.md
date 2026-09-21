# Full solution: Capstone: Define the Product

This worked implementation demonstrates requirements, acceptance criteria, constraints. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Capstone: Define the Product */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool logger_requirements_valid(uint32_t period_ms,uint32_t jitter_ms,size_t record_capacity){return period_ms!=0U&&jitter_ms<=period_ms/10U&&record_capacity>=2U&&record_capacity<=1024U;}
```
