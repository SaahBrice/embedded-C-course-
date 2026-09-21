#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int16_t d[3]={0}; const int16_t s[]={1,2,3,4}; assert(copy_samples(d,3U,s,3U)&&d[2]==3); assert(!copy_samples(d,3U,s,4U)); assert(copy_samples(NULL,0U,NULL,0U));
    
    return 0;
}
