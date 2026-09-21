#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(nonpreemptive_deadline_met(200U,100U,1000U)); assert(nonpreemptive_deadline_met(500U,500U,1000U)); assert(!nonpreemptive_deadline_met(900U,200U,1000U)); assert(!nonpreemptive_deadline_met(1001U,0U,1000U));
    
    return 0;
}
