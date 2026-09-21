#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int32_t out=0; assert(linked_increment(0,&out)&&out==1); assert(linked_increment(-2,&out)&&out==-1); assert(!linked_increment(INT32_MAX,&out)); assert(!linked_increment(1,NULL));
    
    return 0;
}
