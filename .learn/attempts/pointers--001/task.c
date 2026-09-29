#include "task.h"


bool checked_sum(const int32_t *values, size_t count, int64_t *out_sum){
    if (out_sum == NULL) return false;
    if (values == NULL && count != 0U ) return false;
    if (count > (SIZE_MAX / sizeof(*values))) return false;
    int64_t result = 0U;
    for (size_t i = 0U; i < count; i++)
    {
        result += values[i];
    }
     *out_sum = result;
     return true;
}

/* first we need to know how many elements
are in the array, infact we know if we use 
*/