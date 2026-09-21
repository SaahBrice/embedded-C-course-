#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_packet_header_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define packet_header_valid(...) visible_return_packet_header_valid("packet_header_valid(" #__VA_ARGS__ ")", (packet_header_valid)(__VA_ARGS__))
static bool visible_return_packet_decode_value(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define packet_decode_value(...) visible_return_packet_decode_value("packet_decode_value(" #__VA_ARGS__ ")", (packet_decode_value)(__VA_ARGS__))
static bool visible_return_packet_parse(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define packet_parse(...) visible_return_packet_parse("packet_parse(" #__VA_ARGS__ ")", (packet_parse)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 5

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
    const uint8_t good[]={1U,2U,0x34U,0x12U};uint16_t value=0U;struct parsed_packet out={9U,9U};assert(packet_header_valid(good,4U));assert(packet_decode_value(good,4U,&value)&&value==UINT16_C(0x1234));assert(packet_parse(good,4U,&out)&&out.kind==1U&&out.value==UINT16_C(0x1234));const uint8_t bad[]={2U,2U,0U,0U};assert(!packet_header_valid(bad,4U));assert(!packet_parse(good,3U,&out));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
