# Full solution: Decode Portable Byte Layouts

This worked implementation demonstrates padding, alignment, endianness. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Decode Portable Byte Layouts */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool decode_u32_be(const uint8_t *bytes, size_t length, uint32_t *out_value) {
    if (bytes==NULL||out_value==NULL||length<4U) return false;
    *out_value=((uint32_t)bytes[0]<<24U)|((uint32_t)bytes[1]<<16U)|((uint32_t)bytes[2]<<8U)|(uint32_t)bytes[3]; return true;
}
```
