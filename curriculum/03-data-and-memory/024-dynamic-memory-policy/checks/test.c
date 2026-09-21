#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    bool used[]={true,false,false}; size_t index=99U; assert(fixed_pool_acquire(used,3U,&index)&&index==1U&&used[1]); assert(fixed_pool_acquire(used,3U,&index)&&index==2U); assert(!fixed_pool_acquire(used,3U,&index)); assert(!fixed_pool_acquire(NULL,3U,&index));
    
    return 0;
}
