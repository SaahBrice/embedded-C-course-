# Full solution: Drive Digital I/O

This worked implementation demonstrates mode, input, output, active low. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Drive Digital I/O */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool gpio_output_level(bool command_on, bool active_low) { return active_low ? !command_on : command_on; }
```
