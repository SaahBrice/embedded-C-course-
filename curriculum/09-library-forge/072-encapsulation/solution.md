# Full solution: Hide Library Internals

This worked implementation demonstrates public header, private header, opaque state. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Hide Library Internals */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

struct record_queue { uint8_t data[4]; size_t head,tail,count; };
size_t record_queue_required_bytes(void){return sizeof(struct record_queue);} bool record_queue_init(void *storage,size_t storage_size,record_queue_t **out_queue){if(storage==NULL||out_queue==NULL||storage_size<sizeof(struct record_queue))return false; struct record_queue *q=storage; memset(q,0,sizeof *q); *out_queue=q; return true;} bool record_queue_push(record_queue_t *q,uint8_t value){if(q==NULL||q->count==4U)return false;q->data[q->head]=value;q->head=(q->head+1U)%4U;++q->count;return true;} bool record_queue_pop(record_queue_t *q,uint8_t *out){if(q==NULL||out==NULL||q->count==0U)return false;*out=q->data[q->tail];q->tail=(q->tail+1U)%4U;--q->count;return true;}
```
