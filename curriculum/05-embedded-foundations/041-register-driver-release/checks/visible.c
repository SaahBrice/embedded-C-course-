#include "task.h"
#include "sim_mmio.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_gpio_pin_valid(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define gpio_pin_valid(...) visible_return_gpio_pin_valid("gpio_pin_valid(" #__VA_ARGS__ ")", (gpio_pin_valid)(__VA_ARGS__))
static bool visible_return_gpio_mode_set(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define gpio_mode_set(...) visible_return_gpio_mode_set("gpio_mode_set(" #__VA_ARGS__ ")", (gpio_mode_set)(__VA_ARGS__))
static bool visible_return_gpio_mode_matches(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define gpio_mode_matches(...) visible_return_gpio_mode_matches("gpio_mode_matches(" #__VA_ARGS__ ")", (gpio_mode_matches)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 11

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
    uint32_t out=0U;assert(gpio_pin_valid(15U));assert(!gpio_pin_valid(16U));assert(gpio_mode_set(UINT32_MAX,5U,1U,&out));assert(gpio_mode_matches(out,5U,1U));assert((out&~(UINT32_C(3)<<10U))==(UINT32_MAX&~(UINT32_C(3)<<10U)));assert(!gpio_mode_set(0U,16U,1U,&out));
    sim_mmio_reset(); assert(sim_mmio_write(1U,UINT32_MAX)==SIM_MMIO_OK); uint32_t current=0U,configured=0U; assert(sim_mmio_read(1U,&current)==SIM_MMIO_OK); assert(gpio_mode_set(current,5U,1U,&configured)); assert(sim_mmio_write(1U,configured)==SIM_MMIO_OK); assert(sim_mmio_read(1U,&current)==SIM_MMIO_OK&&((current>>10U)&3U)==1U);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
