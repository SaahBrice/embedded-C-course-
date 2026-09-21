#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_frame_payload_length(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define frame_payload_length(...) visible_return_frame_payload_length("frame_payload_length(" #__VA_ARGS__ ")", (frame_payload_length)(__VA_ARGS__))

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
    const uint8_t good[]={1U,2U,0xaaU,0xbbU}; size_t out=0U; assert(frame_payload_length(good,4U,&out)&&out==2U); const uint8_t bad[]={1U,9U}; assert(!frame_payload_length(bad,2U,&out)); assert(!frame_payload_length(good,1U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
