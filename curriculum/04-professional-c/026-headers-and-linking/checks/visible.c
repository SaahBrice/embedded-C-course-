#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static uint8_t visible_return_crc8_update(const char *call, uint8_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define crc8_update(...) visible_return_crc8_update("crc8_update(" #__VA_ARGS__ ")", (crc8_update)(__VA_ARGS__))

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
    assert(crc8_update(0U, 0U) == 0U); assert(crc8_update(0U, UINT8_C(0x31)) == UINT8_C(0x97)); assert(crc8_update(UINT8_C(0x5a), UINT8_C(0xc3)) == UINT8_C(0xc6));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
