#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_read_u32_le(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define read_u32_le(...) visible_return_read_u32_le("read_u32_le(" #__VA_ARGS__ ")", (read_u32_le)(__VA_ARGS__))

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
    const uint8_t b[] = {0x78U,0x56U,0x34U,0x12U}; uint32_t out = 0U; assert(read_u32_le(b,4U,&out) && out == UINT32_C(0x12345678)); assert(!read_u32_le(b,3U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
