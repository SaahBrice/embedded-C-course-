#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(classify_measurement(20000, false) == ACTION_ACCEPT); assert(classify_measurement(-40001, false) == ACTION_RETRY); assert(classify_measurement(125001, false) == ACTION_RETRY); assert(classify_measurement(20000, true) == ACTION_SHUTDOWN);
    
    return 0;
}
