#include "task.h"
#include "sim_timer.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(deadline_reached(100U,100U)); assert(deadline_reached(101U,100U)); assert(!deadline_reached(99U,100U)); assert(deadline_reached(2U,UINT32_MAX-2U));
    sim_timer_reset(UINT32_MAX-2U); sim_timer_advance(5U); assert(deadline_reached(sim_timer_now(),UINT32_MAX-2U)); assert(sim_timer_elapsed(UINT32_MAX-2U)==5U);
    return 0;
}
