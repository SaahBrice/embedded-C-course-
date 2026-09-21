#include "task.h"
#include "sim_interrupt.h"

#include <assert.h>
#include <limits.h>
#include <string.h>


static void dispatch_to_mailbox(void *context,uint32_t event){interrupt_capture(context,event);}

int main(void) {
    struct interrupt_mailbox box={0U,false}; uint32_t event=0U; interrupt_capture(&box,7U); assert(interrupt_take(&box,&event)&&event==7U); assert(!interrupt_take(&box,&event));
    struct interrupt_mailbox simulated={0U,false}; uint32_t captured=0U; sim_interrupt_reset(); assert(sim_interrupt_register(1U,dispatch_to_mailbox,&simulated)==SIM_INTERRUPT_OK); assert(sim_interrupt_trigger(1U,23U)==SIM_INTERRUPT_DISABLED); assert(sim_interrupt_enable(1U,true)==SIM_INTERRUPT_OK); assert(sim_interrupt_trigger(1U,23U)==SIM_INTERRUPT_OK); assert(interrupt_take(&simulated,&captured)&&captured==23U);
    return 0;
}
