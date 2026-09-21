#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum version_change visible_return_classify_version_change(const char *call, enum version_change value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define classify_version_change(...) visible_return_classify_version_change("classify_version_change(" #__VA_ARGS__ ")", (classify_version_change)(__VA_ARGS__))

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
    assert(classify_version_change(false,false)==VERSION_PATCH); assert(classify_version_change(false,true)==VERSION_MINOR); assert(classify_version_change(true,false)==VERSION_MAJOR); assert(classify_version_change(true,true)==VERSION_MAJOR);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
