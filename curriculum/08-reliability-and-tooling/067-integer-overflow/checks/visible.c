#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_checked_scale(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define checked_scale(...) visible_return_checked_scale("checked_scale(" #__VA_ARGS__ ")", (checked_scale)(__VA_ARGS__))

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
    int32_t out=0; assert(checked_scale(1000,2000,&out)&&out==2000000); assert(checked_scale(-7,6,&out)&&out==-42); assert(!checked_scale(INT32_MAX,2,&out)); assert(!checked_scale(INT32_MIN,-1,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
