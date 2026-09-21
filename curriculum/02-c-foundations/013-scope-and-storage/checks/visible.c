#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_instance_increment(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define instance_increment(...) visible_return_instance_increment("instance_increment(" #__VA_ARGS__ ")", (instance_increment)(__VA_ARGS__))

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
    unsigned a=0U,b=7U; assert(instance_increment(&a)&&a==1U); assert(instance_increment(&b)&&b==8U&&a==1U); a=UINT_MAX; assert(!instance_increment(&a)&&a==UINT_MAX); assert(!instance_increment(NULL));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
