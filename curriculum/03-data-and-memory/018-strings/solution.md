# Full solution: Handle C Strings Explicitly

This worked implementation demonstrates null terminator, buffer capacity, string APIs. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Handle C Strings Explicitly */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool buffer_append(char *destination, size_t capacity, const char *suffix) {
    if (destination == NULL || suffix == NULL || capacity == 0U) return false;
    size_t used = 0U; while (used < capacity && destination[used] != '\0') ++used;
    if (used == capacity) return false;
    const size_t added = strlen(suffix); if (added >= capacity - used) return false;
    memcpy(destination + used, suffix, added + 1U); return true;
}
```
