#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int32_t out=0; assert(checked_scale(1000,2000,&out)&&out==2000000); assert(checked_scale(-7,6,&out)&&out==-42); assert(!checked_scale(INT32_MAX,2,&out)); assert(!checked_scale(INT32_MIN,-1,&out));
    
    return 0;
}
