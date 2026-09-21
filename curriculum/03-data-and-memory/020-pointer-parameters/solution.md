# Full solution: Return Results Through Pointers

This worked implementation demonstrates output parameters, null checks, const pointers. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Return Results Through Pointers */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool decode_u16_le(const uint8_t *bytes, size_t length, uint16_t *out_value) {
    if (bytes == NULL || out_value == NULL || length < 2U) return false;
    *out_value = (uint16_t)((uint16_t)bytes[0] | ((uint16_t)bytes[1] << 8U)); return true;
}
```
