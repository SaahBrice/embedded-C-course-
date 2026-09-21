# Full solution: Validate Untrusted Data

This worked implementation demonstrates length trust boundary, integer conversion, fail closed. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Validate Untrusted Data */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool frame_payload_length(const uint8_t *frame,size_t received,size_t *out_length){if(frame==NULL||out_length==NULL||received<2U)return false;const size_t length=frame[1];if(length>received-2U)return false;*out_length=length;return true;}
```
