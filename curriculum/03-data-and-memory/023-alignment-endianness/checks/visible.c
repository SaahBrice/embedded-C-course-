#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_decode_u32_be(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define decode_u32_be(...) visible_return_decode_u32_be("decode_u32_be(" #__VA_ARGS__ ")", (decode_u32_be)(__VA_ARGS__))

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
    const uint8_t bytes[]={0x12U,0x34U,0x56U,0x78U}; uint32_t out=0U; assert(decode_u32_be(bytes,4U,&out)&&out==UINT32_C(0x12345678)); assert(!decode_u32_be(bytes,3U,&out)); assert(!decode_u32_be(NULL,4U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
