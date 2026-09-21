#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    unsigned a=0U,b=7U; assert(instance_increment(&a)&&a==1U); assert(instance_increment(&b)&&b==8U&&a==1U); a=UINT_MAX; assert(!instance_increment(&a)&&a==UINT_MAX); assert(!instance_increment(NULL));
    
    return 0;
}
