#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct byte_ring r={{0U},0U,0U,0U}; uint8_t out=0U; assert(!byte_ring_pop(&r,&out)); for(uint8_t i=1U;i<=4U;++i) assert(byte_ring_push(&r,i)); assert(!byte_ring_push(&r,5U)); assert(byte_ring_pop(&r,&out)&&out==1U); assert(byte_ring_push(&r,5U)); for(uint8_t i=2U;i<=5U;++i) assert(byte_ring_pop(&r,&out)&&out==i);
    
    return 0;
}
