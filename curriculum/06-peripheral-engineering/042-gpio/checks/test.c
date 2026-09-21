#include "task.h"
#include "sim_gpio.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    assert(gpio_output_level(true,false)); assert(!gpio_output_level(false,false)); assert(!gpio_output_level(true,true)); assert(gpio_output_level(false,true));
    sim_gpio_reset(); assert(sim_gpio_configure(5U,SIM_GPIO_OUTPUT)==SIM_GPIO_OK); assert(sim_gpio_write(5U,gpio_output_level(true,true)?SIM_GPIO_HIGH:SIM_GPIO_LOW)==SIM_GPIO_OK); enum sim_gpio_level observed=SIM_GPIO_HIGH; assert(sim_gpio_read(5U,&observed)==SIM_GPIO_OK&&observed==SIM_GPIO_LOW); assert(sim_gpio_write(SIM_GPIO_PIN_COUNT,SIM_GPIO_HIGH)==SIM_GPIO_RANGE);
    return 0;
}
