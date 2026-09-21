# Full solution: Install and Package a C Library

This worked implementation demonstrates Make, CMake, install layout, export. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
#include "rq.h"
const char *rq_version(void) { return "1.0.0"; }
```
