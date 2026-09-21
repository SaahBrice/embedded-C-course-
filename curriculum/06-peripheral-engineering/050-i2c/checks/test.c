#include "task.h"
#include "sim_i2c.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint8_t byte=0U; assert(i2c_address_byte(0x48U,false,&byte)&&byte==0x90U); assert(i2c_address_byte(0x48U,true,&byte)&&byte==0x91U); assert(!i2c_address_byte(0x80U,true,&byte));
    const uint8_t device_regs[]={UINT8_C(0x10),UINT8_C(0x42)}; uint8_t address_byte=0U,sample=0U; sim_i2c_reset(); assert(i2c_address_byte(UINT8_C(0x48),true,&address_byte)&&address_byte==UINT8_C(0x91)); assert(sim_i2c_attach(UINT8_C(0x48),device_regs,sizeof device_regs)==SIM_I2C_OK); assert(sim_i2c_read_register((uint8_t)(address_byte>>1U),1U,&sample)==SIM_I2C_OK&&sample==UINT8_C(0x42)); sim_i2c_fail_next(SIM_I2C_TIMEOUT); assert(sim_i2c_read_register(UINT8_C(0x48),1U,&sample)==SIM_I2C_TIMEOUT);
    return 0;
}
