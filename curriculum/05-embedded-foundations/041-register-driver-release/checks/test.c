#include "task.h"
#include "sim_mmio.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint32_t out=0U;assert(gpio_pin_valid(15U));assert(!gpio_pin_valid(16U));assert(gpio_mode_set(UINT32_MAX,5U,1U,&out));assert(gpio_mode_matches(out,5U,1U));assert((out&~(UINT32_C(3)<<10U))==(UINT32_MAX&~(UINT32_C(3)<<10U)));assert(!gpio_mode_set(0U,16U,1U,&out));
    sim_mmio_reset(); assert(sim_mmio_write(1U,UINT32_MAX)==SIM_MMIO_OK); uint32_t current=0U,configured=0U; assert(sim_mmio_read(1U,&current)==SIM_MMIO_OK); assert(gpio_mode_set(current,5U,1U,&configured)); assert(sim_mmio_write(1U,configured)==SIM_MMIO_OK); assert(sim_mmio_read(1U,&current)==SIM_MMIO_OK&&((current>>10U)&3U)==1U);
    return 0;
}
