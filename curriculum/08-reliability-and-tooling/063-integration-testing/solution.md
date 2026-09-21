# Full solution: Test Collaborating Modules

This worked implementation demonstrates fakes, contracts, failure injection. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Test Collaborating Modules */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool logger_cycle(const struct logger_ports *ports) {
    if (ports == NULL || ports->read == NULL || ports->store == NULL) return false;
    int32_t value=0;
    return ports->read(ports->context,&value) && ports->store(ports->context,value);
}
```
