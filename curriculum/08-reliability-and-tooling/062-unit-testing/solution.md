# Full solution: Test C Modules in Isolation

This worked implementation demonstrates test fixture, assertion, boundary case. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
#include "task.h"
#include <assert.h>
int main(void){assert(median3(3,1,2)==2);assert(median3(-1,-3,-2)==-2);assert(median3(5,5,1)==5);return 0;}
```
