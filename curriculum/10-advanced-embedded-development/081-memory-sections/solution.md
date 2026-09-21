# Full solution: Place Data Deliberately

This worked implementation demonstrates text, rodata, data, bss, noinit. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Place Data Deliberately */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum object_section choose_object_section(bool writable,bool has_nonzero_initializer,bool retain_across_reset){if(retain_across_reset)return SECTION_NOINIT;if(!writable)return SECTION_RODATA;return has_nonzero_initializer?SECTION_DATA:SECTION_BSS;}
```
