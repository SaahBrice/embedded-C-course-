#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    unsigned char storage[128]; record_queue_t *q=NULL; assert(record_queue_required_bytes()<=sizeof storage); assert(record_queue_init(storage,sizeof storage,&q)); uint8_t out=0U; assert(record_queue_push(q,42U)); assert(record_queue_pop(q,&out)&&out==42U); assert(!record_queue_pop(q,&out)); assert(!record_queue_init(storage,1U,&q));
    
    return 0;
}
