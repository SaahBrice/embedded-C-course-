#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    const int32_t v[] = {4, 5, 6}; int64_t sum = -1; assert(checked_sum(v, 3U, &sum) && sum == 15); assert(checked_sum(NULL, 0U, &sum) && sum == 0); assert(!checked_sum(NULL, 1U, &sum)); assert(!checked_sum(v, SIZE_MAX, &sum)); assert(!checked_sum(v, 3U, NULL));
    
    return 0;
}
