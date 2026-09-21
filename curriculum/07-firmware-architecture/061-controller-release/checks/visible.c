#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_sensor_controller_due(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sensor_controller_due(...) visible_return_sensor_controller_due("sensor_controller_due(" #__VA_ARGS__ ")", (sensor_controller_due)(__VA_ARGS__))
static bool visible_return_sensor_sample_acceptable(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sensor_sample_acceptable(...) visible_return_sensor_sample_acceptable("sensor_sample_acceptable(" #__VA_ARGS__ ")", (sensor_sample_acceptable)(__VA_ARGS__))
static bool visible_return_sensor_controller_update(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define sensor_controller_update(...) visible_return_sensor_controller_update("sensor_controller_update(" #__VA_ARGS__ ")", (sensor_controller_update)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 7

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
    struct sensor_controller c={10U,100U,0U};assert(!sensor_controller_due(&c,109U));assert(sensor_controller_due(&c,110U));assert(sensor_sample_acceptable(true,25,-40,125));assert(!sensor_sample_acceptable(false,25,-40,125));assert(!sensor_sample_acceptable(true,126,-40,125));assert(sensor_controller_update(&c,110U,true)&&c.samples==1U&&c.last_sample==110U);assert(!sensor_controller_update(&c,120U,false));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
