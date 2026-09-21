# Full solution: Decode Binary and Hexadecimal

This worked implementation demonstrates base conversion, bit positions, hex notation. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Decode Binary and Hexadecimal */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint8_t swap_nibbles(uint8_t value) { return (uint8_t)((value << 4U) | (value >> 4U)); }
```
