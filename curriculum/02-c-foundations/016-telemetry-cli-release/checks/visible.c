#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_celsius_in_sensor_range(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define celsius_in_sensor_range(...) visible_return_celsius_in_sensor_range("celsius_in_sensor_range(" #__VA_ARGS__ ")", (celsius_in_sensor_range)(__VA_ARGS__))
static bool visible_return_celsius_to_milli(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define celsius_to_milli(...) visible_return_celsius_to_milli("celsius_to_milli(" #__VA_ARGS__ ")", (celsius_to_milli)(__VA_ARGS__))
static bool visible_return_telemetry_prepare(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define telemetry_prepare(...) visible_return_telemetry_prepare("telemetry_prepare(" #__VA_ARGS__ ")", (telemetry_prepare)(__VA_ARGS__))

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
    int32_t v=77;assert(celsius_in_sensor_range(-40.0));assert(!celsius_in_sensor_range(125.1));assert(celsius_to_milli(21.125,&v)&&v==21125);assert(celsius_to_milli(-0.0006,&v)&&v==-1);v=77;assert(telemetry_prepare(3.3,false,&v)&&v==3300);assert(!telemetry_prepare(3.3,true,&v)&&v==3300);
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
