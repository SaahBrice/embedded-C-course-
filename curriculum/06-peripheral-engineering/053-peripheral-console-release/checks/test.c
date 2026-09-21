#include "task.h"
#include "sim_uart.h"
#include "sim_gpio.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    bool level=false;assert(console_parse("LED ON")==CONSOLE_LED_ON);assert(console_parse("READ ADC")==CONSOLE_READ_ADC);assert(console_is_led_command(CONSOLE_LED_OFF));assert(!console_is_led_command(CONSOLE_READ_ADC));assert(console_led_level(CONSOLE_LED_ON,false,&level)&&level);assert(console_led_level(CONSOLE_LED_ON,true,&level)&&!level);assert(!console_led_level(CONSOLE_READ_ADC,false,&level));assert(console_parse("LED")==CONSOLE_INVALID);
    const uint8_t command[]={'L','E','D',' ','O','N'}; uint8_t line[7]={0U}; sim_uart_reset(); sim_gpio_reset(); assert(sim_uart_inject_rx(command,sizeof command)==SIM_UART_OK); for(size_t index=0U;index<sizeof command;++index)assert(sim_uart_read(&line[index])==SIM_UART_OK); assert(console_parse((const char *)line)==CONSOLE_LED_ON); assert(sim_gpio_configure(5U,SIM_GPIO_OUTPUT)==SIM_GPIO_OK); assert(sim_gpio_write(5U,SIM_GPIO_HIGH)==SIM_GPIO_OK); enum sim_gpio_level led=SIM_GPIO_LOW; assert(sim_gpio_read(5U,&led)==SIM_GPIO_OK&&led==SIM_GPIO_HIGH);
    return 0;
}
