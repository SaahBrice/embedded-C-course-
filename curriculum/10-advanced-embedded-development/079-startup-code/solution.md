# Full solution: Follow MCU Startup

This worked implementation demonstrates reset handler, vector table, C runtime. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Follow MCU Startup */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool zero_bss_words(uint32_t *words,size_t count){if(words==NULL&&count!=0U)return false;for(size_t i=0U;i<count;++i)words[i]=0U;return true;}
```
