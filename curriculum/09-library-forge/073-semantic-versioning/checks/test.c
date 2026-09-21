#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(classify_version_change(false,false)==VERSION_PATCH); assert(classify_version_change(false,true)==VERSION_MINOR); assert(classify_version_change(true,false)==VERSION_MAJOR); assert(classify_version_change(true,true)==VERSION_MAJOR);
    
    return 0;
}
