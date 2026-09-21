#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    volatile uint32_t reg=UINT32_C(0xa5); uint32_t out=0U; assert(sample_volatile_register(&reg,&out)&&out==UINT32_C(0xa5)); reg=7U; assert(sample_volatile_register(&reg,&out)&&out==7U); assert(!sample_volatile_register(NULL,&out));
    
    return 0;
}
