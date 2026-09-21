#include "task.h"
#include "sim_timer.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_blinker_update(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define blinker_update(...) visible_return_blinker_update("blinker_update(" #__VA_ARGS__ ")", (blinker_update)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 4

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
    struct blinker b = {10U,5U,false}; assert(!blinker_update(&b,14U) && !b.level); assert(blinker_update(&b,15U) && b.level && b.last_change == 15U); b.last_change=UINT32_MAX-2U; b.period=5U; assert(blinker_update(&b,2U));
    struct blinker timed={UINT32_MAX-2U,5U,false}; sim_timer_reset(UINT32_MAX-2U); sim_timer_advance(5U); assert(blinker_update(&timed,sim_timer_now())&&timed.level);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
