#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_nonpreemptive_deadline_met(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define nonpreemptive_deadline_met(...) visible_return_nonpreemptive_deadline_met("nonpreemptive_deadline_met(" #__VA_ARGS__ ")", (nonpreemptive_deadline_met)(__VA_ARGS__))

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
    assert(nonpreemptive_deadline_met(200U,100U,1000U)); assert(nonpreemptive_deadline_met(500U,500U,1000U)); assert(!nonpreemptive_deadline_met(900U,200U,1000U)); assert(!nonpreemptive_deadline_met(1001U,0U,1000U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
