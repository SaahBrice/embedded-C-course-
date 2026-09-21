# Full solution: Model Behavior as States

This worked implementation demonstrates state, event, transition, guard. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Model Behavior as States */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum controller_state controller_transition(enum controller_state state, enum controller_event event) {
    switch (state) { case CONTROLLER_IDLE: return event == EVENT_START ? CONTROLLER_SAMPLING : (event == EVENT_RESET ? CONTROLLER_IDLE : CONTROLLER_FAULT); case CONTROLLER_SAMPLING: if (event == EVENT_SAMPLE_OK) return CONTROLLER_IDLE; if (event == EVENT_SAMPLE_BAD) return CONTROLLER_FAULT; return state; case CONTROLLER_FAULT: return event == EVENT_RESET ? CONTROLLER_IDLE : CONTROLLER_FAULT; default: return CONTROLLER_FAULT; }
}
```
