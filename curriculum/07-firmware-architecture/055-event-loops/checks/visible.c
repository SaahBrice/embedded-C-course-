#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_task_due(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define task_due(...) visible_return_task_due("task_due(" #__VA_ARGS__ ")", (task_due)(__VA_ARGS__))

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
    assert(!task_due(14U,10U,5U)); assert(task_due(15U,10U,5U)); assert(task_due(2U,UINT32_MAX-2U,5U)); assert(!task_due(10U,0U,0U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
