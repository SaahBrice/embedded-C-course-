#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>

static uint32_t fake_clock(void *context){return *(uint32_t *)context;}


int main(void) {
    uint32_t clock=1234U; struct timestamped_value r={0U,0}; assert(timestamp_record(fake_clock,&clock,-7,&r)&&r.timestamp_ms==1234U&&r.value==-7); assert(!timestamp_record(NULL,&clock,1,&r));
    
    return 0;
}
