#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_scheduler_release(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define scheduler_release(...) visible_return_scheduler_release("scheduler_release(" #__VA_ARGS__ ")", (scheduler_release)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 3

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
    struct scheduled_task t={10U,100U,0U}; assert(!scheduler_release(&t,99U)); assert(scheduler_release(&t,100U)&&t.next_release==110U&&t.runs==1U); t.next_release=UINT32_MAX-2U;t.period=5U;assert(scheduler_release(&t,2U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
