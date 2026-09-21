#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_fixed_pool_acquire(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define fixed_pool_acquire(...) visible_return_fixed_pool_acquire("fixed_pool_acquire(" #__VA_ARGS__ ")", (fixed_pool_acquire)(__VA_ARGS__))

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
    bool used[]={true,false,false}; size_t index=99U; assert(fixed_pool_acquire(used,3U,&index)&&index==1U&&used[1]); assert(fixed_pool_acquire(used,3U,&index)&&index==2U); assert(!fixed_pool_acquire(used,3U,&index)); assert(!fixed_pool_acquire(NULL,3U,&index));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
