#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint8_t d[4] = {0U}; const uint8_t s[] = {1U,2U,3U}; assert(bounded_copy(d,4U,s,3U) && d[2] == 3U); assert(!bounded_copy(d,2U,s,3U)); assert(bounded_copy(NULL,0U,NULL,0U));
    
    return 0;
}
