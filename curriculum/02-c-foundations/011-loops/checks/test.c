#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const int16_t v[] = {3, 6, 9, 12}; int32_t avg = 0; assert(sample_average(v, 4U, &avg) && avg == 7); assert(!sample_average(v, 0U, &avg)); assert(!sample_average(NULL, 1U, &avg));
    
    return 0;
}
