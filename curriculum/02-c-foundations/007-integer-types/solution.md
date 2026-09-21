# Full solution: Choose Integer Types Deliberately

This worked implementation demonstrates signedness, range, integer promotion. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Choose Integer Types Deliberately */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool temperature_fits_i16(int32_t milli_celsius) { return milli_celsius >= INT16_MIN && milli_celsius <= INT16_MAX; }
```
