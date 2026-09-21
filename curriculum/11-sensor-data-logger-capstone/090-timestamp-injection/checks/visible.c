#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>

static uint32_t fake_clock(void *context){return *(uint32_t *)context;}

static bool visible_return_timestamp_record(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define timestamp_record(...) visible_return_timestamp_record("timestamp_record(" #__VA_ARGS__ ")", (timestamp_record)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 2

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
    uint32_t clock=1234U; struct timestamped_value r={0U,0}; assert(timestamp_record(fake_clock,&clock,-7,&r)&&r.timestamp_ms==1234U&&r.value==-7); assert(!timestamp_record(NULL,&clock,1,&r));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
