#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static uint8_t visible_return_swap_nibbles(const char *call, uint8_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define swap_nibbles(...) visible_return_swap_nibbles("swap_nibbles(" #__VA_ARGS__ ")", (swap_nibbles)(__VA_ARGS__))

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
    assert(swap_nibbles(UINT8_C(0xa5))==UINT8_C(0x5a)); assert(swap_nibbles(UINT8_C(0xf0))==UINT8_C(0x0f)); assert(swap_nibbles(0U)==0U);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
