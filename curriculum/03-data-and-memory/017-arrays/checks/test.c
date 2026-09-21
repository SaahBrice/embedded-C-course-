#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const int16_t v[] = {7, -2, 19, 4}; int16_t low = 0, high = 0; assert(sample_minmax(v, 4U, &low, &high) && low == -2 && high == 19); assert(sample_minmax(v, 1U, &low, &high) && low == 7 && high == 7); assert(!sample_minmax(v, 0U, &low, &high));
    
    return 0;
}
