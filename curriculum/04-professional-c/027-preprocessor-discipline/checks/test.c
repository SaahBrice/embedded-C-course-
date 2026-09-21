#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(square_i16_once(0)==0); assert(square_i16_once(-3)==9); assert(square_i16_once(INT16_MAX)==INT32_C(1073676289)); assert(square_i16_once(INT16_MIN)==INT32_C(1073741824));
    
    return 0;
}
