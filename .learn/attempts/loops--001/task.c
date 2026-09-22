#include "task.h"

bool sample_average(const int16_t *samples, size_t count, int32_t *out_average){
    if(samples==NULL || out_average==NULL || count<=1U)return false;
    int64_t total =0;
    for (size_t i =0U; i<count; ++i) total +=samples[i];
    *out_average = (int32_t)(total/(int64_t)count);
    return true;
}


/* TODO — Process a Sample Window: implement the declared interface.
 * Contract to prove: The loop invariant is that `total` contains exactly the first `i` samples; an empty window has no average.
 */
