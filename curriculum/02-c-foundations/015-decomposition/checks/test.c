#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int32_t out=0; assert(scale_offset_sample(10,-2,3,&out)&&out==24); assert(scale_offset_sample(-5,5,9,&out)&&out==0); assert(!scale_offset_sample(INT32_MAX,1,1,&out)); assert(!scale_offset_sample(1,1,1,NULL));
    
    return 0;
}
