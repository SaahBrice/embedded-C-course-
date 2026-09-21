#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(!task_due(14U,10U,5U)); assert(task_due(15U,10U,5U)); assert(task_due(2U,UINT32_MAX-2U,5U)); assert(!task_due(10U,0U,0U));
    
    return 0;
}
