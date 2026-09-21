#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static uint32_t visible_return_status_bits_update(const char *call, uint32_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define status_bits_update(...) visible_return_status_bits_update("status_bits_update(" #__VA_ARGS__ ")", (status_bits_update)(__VA_ARGS__))

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
    assert(status_bits_update(UINT32_C(0x0a), UINT32_C(0x05), UINT32_C(0x08)) == UINT32_C(0x07)); assert(status_bits_update(UINT32_MAX, 0U, UINT32_MAX) == 0U);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
