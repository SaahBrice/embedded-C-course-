#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    unsigned out=0U; assert(counter_add_bounded(3U,4U,10U,&out)&&out==7U); assert(counter_add_bounded(10U,0U,10U,&out)&&out==10U); assert(!counter_add_bounded(9U,2U,10U,&out));
    
    return 0;
}
