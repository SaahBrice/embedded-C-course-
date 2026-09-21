#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(clamp_i32(5, 0, 10) == 5); assert(clamp_i32(-1, 0, 10) == 0); assert(clamp_i32(11, 0, 10) == 10); assert(clamp_i32(4, 7, 3) == 7);
    
    return 0;
}
