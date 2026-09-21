#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_copy_samples(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define copy_samples(...) visible_return_copy_samples("copy_samples(" #__VA_ARGS__ ")", (copy_samples)(__VA_ARGS__))

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
    int16_t d[3]={0}; const int16_t s[]={1,2,3,4}; assert(copy_samples(d,3U,s,3U)&&d[2]==3); assert(!copy_samples(d,3U,s,4U)); assert(copy_samples(NULL,0U,NULL,0U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
