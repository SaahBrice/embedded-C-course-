#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint8_t out[3]={0}; const uint8_t in[]={1U,2U,3U}; assert(documented_copy(out,3U,in,3U)&&out[2]==3U); assert(!documented_copy(out,2U,in,3U)); assert(documented_copy(NULL,0U,NULL,0U));
    
    return 0;
}
