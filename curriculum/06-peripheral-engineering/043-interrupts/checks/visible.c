#include "task.h"
#include "sim_interrupt.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>


static void dispatch_to_mailbox(void *context,uint32_t event){interrupt_capture(context,event);}
#define interrupt_capture(...) (printf("Call and inputs: %s\n  Actual return: void\n", "interrupt_capture(" #__VA_ARGS__ ")"), (interrupt_capture)(__VA_ARGS__))
static bool visible_return_interrupt_take(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define interrupt_take(...) visible_return_interrupt_take("interrupt_take(" #__VA_ARGS__ ")", (interrupt_take)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 7

static unsigned visible_case_number;
static unsigned visible_failures;

static void visible_check(int passed, const char *expression) {
    printf("Case %u\n  Expected condition: %s\n  Observed condition: %s\n  Result: %s\n",
           visible_case_number, expression, passed ? "true" : "false",
           passed ? "PASS" : "FAIL");
    if (!passed) ++visible_failures;
}

#define assert(expression) do {     ++visible_case_number;     visible_check(!!(expression), #expression); } while (0)

int main(void) {
    struct interrupt_mailbox box={0U,false}; uint32_t event=0U; interrupt_capture(&box,7U); assert(interrupt_take(&box,&event)&&event==7U); assert(!interrupt_take(&box,&event));
    struct interrupt_mailbox simulated={0U,false}; uint32_t captured=0U; sim_interrupt_reset(); assert(sim_interrupt_register(1U,dispatch_to_mailbox,&simulated)==SIM_INTERRUPT_OK); assert(sim_interrupt_trigger(1U,23U)==SIM_INTERRUPT_DISABLED); assert(sim_interrupt_enable(1U,true)==SIM_INTERRUPT_OK); assert(sim_interrupt_trigger(1U,23U)==SIM_INTERRUPT_OK); assert(interrupt_take(&simulated,&captured)&&captured==23U);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
