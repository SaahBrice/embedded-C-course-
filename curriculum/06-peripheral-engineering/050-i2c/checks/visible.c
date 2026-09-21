#include "task.h"
#include "sim_i2c.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_i2c_address_byte(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define i2c_address_byte(...) visible_return_i2c_address_byte("i2c_address_byte(" #__VA_ARGS__ ")", (i2c_address_byte)(__VA_ARGS__))

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
    uint8_t byte=0U; assert(i2c_address_byte(0x48U,false,&byte)&&byte==0x90U); assert(i2c_address_byte(0x48U,true,&byte)&&byte==0x91U); assert(!i2c_address_byte(0x80U,true,&byte));
    const uint8_t device_regs[]={UINT8_C(0x10),UINT8_C(0x42)}; uint8_t address_byte=0U,sample=0U; sim_i2c_reset(); assert(i2c_address_byte(UINT8_C(0x48),true,&address_byte)&&address_byte==UINT8_C(0x91)); assert(sim_i2c_attach(UINT8_C(0x48),device_regs,sizeof device_regs)==SIM_I2C_OK); assert(sim_i2c_read_register((uint8_t)(address_byte>>1U),1U,&sample)==SIM_I2C_OK&&sample==UINT8_C(0x42)); sim_i2c_fail_next(SIM_I2C_TIMEOUT); assert(sim_i2c_read_register(UINT8_C(0x48),1U,&sample)==SIM_I2C_TIMEOUT);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
