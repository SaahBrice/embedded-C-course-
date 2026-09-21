#include "task.h"
#include "sim_timer.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct blinker b = {10U,5U,false}; assert(!blinker_update(&b,14U) && !b.level); assert(blinker_update(&b,15U) && b.level && b.last_change == 15U); b.last_change=UINT32_MAX-2U; b.period=5U; assert(blinker_update(&b,2U));
    struct blinker timed={UINT32_MAX-2U,5U,false}; sim_timer_reset(UINT32_MAX-2U); sim_timer_advance(5U); assert(blinker_update(&timed,sim_timer_now())&&timed.level);
    return 0;
}
