# Full solution: Transact over I2C

This worked implementation demonstrates address, start stop, ACK NACK. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Transact over I2C */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool i2c_address_byte(uint8_t address_7bit, bool read, uint8_t *out_byte) {
    if (out_byte == NULL || address_7bit > 0x7fU) return false;
    *out_byte = (uint8_t)((address_7bit << 1U) | (read ? 1U : 0U));
    return true;
}
```
