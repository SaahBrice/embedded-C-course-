# Full solution: Validate External Input

This worked implementation demonstrates strtol, end pointers, range checks. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Validate External Input */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool parse_u16(const char *text, uint16_t *out_value) {
    if (text == NULL || out_value == NULL || text[0] == '\0' || text[0] == '-') return false;
    errno = 0; char *end = NULL; const unsigned long parsed = strtoul(text, &end, 10);
    if (errno != 0 || end == text || *end != '\0' || parsed > UINT16_MAX) return false;
    *out_value = (uint16_t)parsed; return true;
}
```
