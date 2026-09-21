# Full solution: Capstone: Export Reliably

This worked implementation demonstrates transport port, bounded retry, backoff. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Capstone: Export Reliably */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum transport_status transport_retry(transport_send_fn send,void *context,unsigned max_attempts,unsigned *out_attempts){if(send==NULL||out_attempts==NULL||max_attempts==0U)return TRANSPORT_PERMANENT;for(unsigned n=1U;n<=max_attempts;++n){enum transport_status s=send(context);*out_attempts=n;if(s!=TRANSPORT_TEMPORARY)return s;}return TRANSPORT_TEMPORARY;}
```
