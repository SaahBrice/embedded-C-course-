#include "task.h"
#include "sim_timer.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_deadline_reached(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define deadline_reached(...) visible_return_deadline_reached("deadline_reached(" #__VA_ARGS__ ")", (deadline_reached)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 6

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
    assert(deadline_reached(100U,100U)); assert(deadline_reached(101U,100U)); assert(!deadline_reached(99U,100U)); assert(deadline_reached(2U,UINT32_MAX-2U));
    sim_timer_reset(UINT32_MAX-2U); sim_timer_advance(5U); assert(deadline_reached(sim_timer_now(),UINT32_MAX-2U)); assert(sim_timer_elapsed(UINT32_MAX-2U)==5U);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
