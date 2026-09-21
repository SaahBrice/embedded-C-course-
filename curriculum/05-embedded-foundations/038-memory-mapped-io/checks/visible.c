#include "task.h"
#include "sim_mmio.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_register_update(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define register_update(...) visible_return_register_update("register_update(" #__VA_ARGS__ ")", (register_update)(__VA_ARGS__))

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
    volatile uint32_t reg = UINT32_C(0xf0); assert(register_update(&reg,UINT32_C(0x30),UINT32_C(0x05)) && reg == UINT32_C(0xc5)); assert(!register_update(NULL,0U,0U));
    sim_mmio_reset(); assert(sim_mmio_write(4U,UINT32_C(0xf0))==SIM_MMIO_OK); uint32_t mmio=0U; assert(sim_mmio_read(4U,&mmio)==SIM_MMIO_OK); volatile uint32_t work=mmio; assert(register_update(&work,UINT32_C(0x30),UINT32_C(0x05))); assert(sim_mmio_write(4U,work)==SIM_MMIO_OK); assert(sim_mmio_read(4U,&mmio)==SIM_MMIO_OK&&mmio==UINT32_C(0xc5));
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
