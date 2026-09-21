#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct record_ring q={{{0U,0}},0U,0U,0U}; struct log_record out={0U,0}; for(int32_t i=1;i<=3;++i)assert(record_ring_push(&q,(struct log_record){(uint32_t)i,i}));assert(!record_ring_push(&q,(struct log_record){4U,4}));assert(record_ring_pop(&q,&out)&&out.value==1);assert(record_ring_push(&q,(struct log_record){4U,4}));for(int32_t i=2;i<=4;++i)assert(record_ring_pop(&q,&out)&&out.value==i);
    
    return 0;
}
