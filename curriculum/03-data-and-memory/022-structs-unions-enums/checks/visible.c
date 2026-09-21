#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_packet_value(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define packet_value(...) visible_return_packet_value("packet_value(" #__VA_ARGS__ ")", (packet_value)(__VA_ARGS__))

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
    struct sensor_packet t = {PACKET_TEMPERATURE, {.temperature_centi_c = -125}}; int32_t value = 0;
assert(packet_value(&t, &value) && value == -125); struct sensor_packet h = {PACKET_HUMIDITY, {.humidity_centi_percent = 4567U}}; assert(packet_value(&h, &value) && value == 4567); t.kind = (enum packet_kind)99; assert(!packet_value(&t, &value));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
