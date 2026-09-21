#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_queue_storage_size(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define queue_storage_size(...) visible_return_queue_storage_size("queue_storage_size(" #__VA_ARGS__ ")", (queue_storage_size)(__VA_ARGS__))

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
    size_t out=9U; assert(queue_storage_size(8U,12U,&out)&&out==96U); assert(queue_storage_size(0U,12U,&out)&&out==0U); assert(!queue_storage_size(SIZE_MAX,2U,&out)); assert(!queue_storage_size(1U,1U,NULL));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
