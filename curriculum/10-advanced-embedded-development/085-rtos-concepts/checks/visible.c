#include "task.h"


#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_startup_services_ready(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define startup_services_ready(...) visible_return_startup_services_ready("startup_services_ready(" #__VA_ARGS__ ")", (startup_services_ready)(__VA_ARGS__))
static bool visible_return_queue_absorbs_burst(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define queue_absorbs_burst(...) visible_return_queue_absorbs_burst("queue_absorbs_burst(" #__VA_ARGS__ ")", (queue_absorbs_burst)(__VA_ARGS__))
static bool visible_return_periodic_load_fits(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define periodic_load_fits(...) visible_return_periodic_load_fits("periodic_load_fits(" #__VA_ARGS__ ")", (periodic_load_fits)(__VA_ARGS__))
static bool visible_return_rtos_partition_justified(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define rtos_partition_justified(...) visible_return_rtos_partition_justified("rtos_partition_justified(" #__VA_ARGS__ ")", (rtos_partition_justified)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 10

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
    assert(startup_services_ready(true,true,true));assert(!startup_services_ready(true,false,true));assert(queue_absorbs_burst(8U,3U,5U));assert(!queue_absorbs_burst(9U,3U,5U));assert(periodic_load_fits(200U,100U,1000U));assert(!periodic_load_fits(900U,200U,1000U));assert(rtos_partition_justified(3U,true,true));assert(rtos_partition_justified(2U,false,false));assert(!rtos_partition_justified(1U,true,false));assert(!rtos_partition_justified(3U,false,true));
    
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
