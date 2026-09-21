#include "task.h"
#include "sim_mmio.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    volatile uint32_t reg = UINT32_C(0xf0); assert(register_update(&reg,UINT32_C(0x30),UINT32_C(0x05)) && reg == UINT32_C(0xc5)); assert(!register_update(NULL,0U,0U));
    sim_mmio_reset(); assert(sim_mmio_write(4U,UINT32_C(0xf0))==SIM_MMIO_OK); uint32_t mmio=0U; assert(sim_mmio_read(4U,&mmio)==SIM_MMIO_OK); volatile uint32_t work=mmio; assert(register_update(&work,UINT32_C(0x30),UINT32_C(0x05))); assert(sim_mmio_write(4U,work)==SIM_MMIO_OK); assert(sim_mmio_read(4U,&mmio)==SIM_MMIO_OK&&mmio==UINT32_C(0xc5));
    return 0;
}
