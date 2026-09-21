#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    int32_t v[]={1,2,1,3}; assert(replace_value(v,4U,1,9)==2U); assert(v[0]==9&&v[1]==2&&v[2]==9&&v[3]==3); assert(replace_value(v,0U,9,0)==0U); assert(replace_value(NULL,4U,1,2)==0U);
    
    return 0;
}
