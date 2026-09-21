#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_checked_array_read(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define checked_array_read(...) visible_return_checked_array_read("checked_array_read(" #__VA_ARGS__ ")", (checked_array_read)(__VA_ARGS__))

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
    const int32_t values[]={4,8,15}; int32_t out=0; assert(checked_array_read(values,3U,2U,&out)&&out==15); assert(!checked_array_read(values,3U,3U,&out)); assert(!checked_array_read(NULL,3U,0U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
