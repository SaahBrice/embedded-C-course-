#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct scheduled_task t={10U,100U,0U}; assert(!scheduler_release(&t,99U)); assert(scheduler_release(&t,100U)&&t.next_release==110U&&t.runs==1U); t.next_release=UINT32_MAX-2U;t.period=5U;assert(scheduler_release(&t,2U));
    
    return 0;
}
