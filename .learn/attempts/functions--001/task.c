#include "task.h"

int32_t clamp_i32(int32_t value, int32_t minimum, int32_t maximum){
    if (value <= minimum){
        return minimum;
    } else if (value >= maximum)
    {
        return maximum;
    } else return value;
    
}

/* TODO — Extract Testable Functions: implement the declared interface.
 * Contract to prove: `clamp_i32` is a pure, independently testable calculation with explicit behavior for an invalid interval.
 */
