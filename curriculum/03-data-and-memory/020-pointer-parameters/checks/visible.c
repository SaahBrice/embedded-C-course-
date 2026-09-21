#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_decode_u16_le(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define decode_u16_le(...) visible_return_decode_u16_le("decode_u16_le(" #__VA_ARGS__ ")", (decode_u16_le)(__VA_ARGS__))

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
    const uint8_t bytes[] = {0x34U, 0x12U}; uint16_t value = 0U; assert(decode_u16_le(bytes, 2U, &value) && value == UINT16_C(0x1234)); assert(!decode_u16_le(bytes, 1U, &value)); assert(!decode_u16_le(NULL, 2U, &value));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
