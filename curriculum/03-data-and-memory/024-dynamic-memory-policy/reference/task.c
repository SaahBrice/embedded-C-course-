/* Mission: Set an Allocation Policy */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool fixed_pool_acquire(bool *used, size_t capacity, size_t *out_index) {
    if (used==NULL||out_index==NULL||capacity==0U) return false;
    for(size_t i=0U;i<capacity;++i) if(!used[i]){used[i]=true;*out_index=i;return true;}
    return false;
}
