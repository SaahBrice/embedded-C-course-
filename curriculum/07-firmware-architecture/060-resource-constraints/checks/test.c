#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    size_t out=9U; assert(queue_storage_size(8U,12U,&out)&&out==96U); assert(queue_storage_size(0U,12U,&out)&&out==0U); assert(!queue_storage_size(SIZE_MAX,2U,&out)); assert(!queue_storage_size(1U,1U,NULL));
    
    return 0;
}
