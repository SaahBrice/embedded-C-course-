#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_record_serialize(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define record_serialize(...) visible_return_record_serialize("record_serialize(" #__VA_ARGS__ ")", (record_serialize)(__VA_ARGS__))

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
    struct serial_record r={UINT32_C(0x12345678),-2}; uint8_t b[RECORD_WIRE_SIZE]={0U}; assert(record_serialize(&r,b,sizeof b)); const uint8_t expected[]={1U,0x78U,0x56U,0x34U,0x12U,0xfeU,0xffU,0xffU,0xffU}; assert(memcmp(b,expected,sizeof b)==0); assert(!record_serialize(&r,b,8U));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
