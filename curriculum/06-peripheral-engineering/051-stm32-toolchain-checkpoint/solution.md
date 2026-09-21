# Full solution: Prepare the STM32 Toolchain

This worked implementation demonstrates ARM compiler, debug probe, OpenOCD, Cube tools. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Prepare the STM32 Toolchain */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool elf_header_targets_arm(const uint8_t *header,size_t length){return header!=NULL&&length>=20U&&header[0]==0x7fU&&header[1]=='E'&&header[2]=='L'&&header[3]=='F'&&header[18]==0x28U&&header[19]==0U;}
```
