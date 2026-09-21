#include "task.h"
#include "sim_gpio.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_gpio_output_level(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define gpio_output_level(...) visible_return_gpio_output_level("gpio_output_level(" #__VA_ARGS__ ")", (gpio_output_level)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 8

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
    assert(gpio_output_level(true,false)); assert(!gpio_output_level(false,false)); assert(!gpio_output_level(true,true)); assert(gpio_output_level(false,true));
    sim_gpio_reset(); assert(sim_gpio_configure(5U,SIM_GPIO_OUTPUT)==SIM_GPIO_OK); assert(sim_gpio_write(5U,gpio_output_level(true,true)?SIM_GPIO_HIGH:SIM_GPIO_LOW)==SIM_GPIO_OK); enum sim_gpio_level observed=SIM_GPIO_HIGH; assert(sim_gpio_read(5U,&observed)==SIM_GPIO_OK&&observed==SIM_GPIO_LOW); assert(sim_gpio_write(SIM_GPIO_PIN_COUNT,SIM_GPIO_HIGH)==SIM_GPIO_RANGE);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
