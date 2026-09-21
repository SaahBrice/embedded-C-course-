#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const int32_t values[]={4,8,15}; int32_t out=0; assert(checked_array_read(values,3U,2U,&out)&&out==15); assert(!checked_array_read(values,3U,3U,&out)); assert(!checked_array_read(NULL,3U,0U,&out));
    
    return 0;
}
