# Full solution: Document Contracts and Examples

This worked implementation demonstrates preconditions, ownership, thread context, examples. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Document Contracts and Examples */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool documented_copy(uint8_t *destination,size_t capacity,const uint8_t *source,size_t count){if(count>capacity||(count!=0U&&(destination==NULL||source==NULL)))return false;if(count!=0U)memcpy(destination,source,count);return true;}
```
