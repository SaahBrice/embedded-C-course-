#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_scale_offset_sample(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define scale_offset_sample(...) visible_return_scale_offset_sample("scale_offset_sample(" #__VA_ARGS__ ")", (scale_offset_sample)(__VA_ARGS__))

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
    int32_t out=0; assert(scale_offset_sample(10,-2,3,&out)&&out==24); assert(scale_offset_sample(-5,5,9,&out)&&out==0); assert(!scale_offset_sample(INT32_MAX,1,1,&out)); assert(!scale_offset_sample(1,1,1,NULL));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
