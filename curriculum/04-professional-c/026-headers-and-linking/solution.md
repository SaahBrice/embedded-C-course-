# Full solution: Separate Interface from Implementation

This worked implementation demonstrates headers, translation units, linkage. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Separate Interface from Implementation */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint8_t crc8_update(uint8_t crc, uint8_t byte) {
    crc ^= byte; for (unsigned bit = 0U; bit < 8U; ++bit) crc = (uint8_t)((crc & 0x80U) ? (uint8_t)(crc << 1U) ^ 0x07U : (uint8_t)(crc << 1U)); return crc;
}
```
