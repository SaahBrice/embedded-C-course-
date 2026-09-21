# Full solution: Connect Firmware to Electronics

This worked implementation demonstrates voltage, current, pull resistors, active levels. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Connect Firmware to Electronics */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool led_output_level(bool active_low,bool led_on){return active_low?!led_on:led_on;}
```
