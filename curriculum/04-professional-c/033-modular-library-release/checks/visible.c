#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static uint8_t visible_return_crc8_update(const char *call, uint8_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define crc8_update(...) visible_return_crc8_update("crc8_update(" #__VA_ARGS__ ")", (crc8_update)(__VA_ARGS__))
static uint8_t visible_return_crc8(const char *call, uint8_t value) { printf("Call and inputs: %s\n  Actual return: %llu\n", call, (unsigned long long)value); return value; }
#define crc8(...) visible_return_crc8("crc8(" #__VA_ARGS__ ")", (crc8)(__VA_ARGS__))
static bool visible_return_crc8_verify(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define crc8_verify(...) visible_return_crc8_verify("crc8_verify(" #__VA_ARGS__ ")", (crc8_verify)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 6

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
    const uint8_t data[]={1U,2U,3U};assert(crc8_update(0U,1U)==UINT8_C(0x07));assert(crc8(data,3U)==UINT8_C(0x48));assert(crc8(NULL,0U)==0U);assert(crc8_verify(data,3U,UINT8_C(0x48)));assert(!crc8_verify(data,3U,UINT8_C(0x49)));assert(!crc8_verify(NULL,1U,0U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
