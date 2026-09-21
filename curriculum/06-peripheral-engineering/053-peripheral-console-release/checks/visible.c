#include "task.h"
#include "sim_uart.h"
#include "sim_gpio.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static enum console_command visible_return_console_parse(const char *call, enum console_command value) { printf("Call and inputs: %s\n  Actual return: %lld\n", call, (long long)value); return value; }
#define console_parse(...) visible_return_console_parse("console_parse(" #__VA_ARGS__ ")", (console_parse)(__VA_ARGS__))
static bool visible_return_console_is_led_command(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define console_is_led_command(...) visible_return_console_is_led_command("console_is_led_command(" #__VA_ARGS__ ")", (console_is_led_command)(__VA_ARGS__))
static bool visible_return_console_led_level(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define console_led_level(...) visible_return_console_led_level("console_led_level(" #__VA_ARGS__ ")", (console_led_level)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 14

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
    bool level=false;assert(console_parse("LED ON")==CONSOLE_LED_ON);assert(console_parse("READ ADC")==CONSOLE_READ_ADC);assert(console_is_led_command(CONSOLE_LED_OFF));assert(!console_is_led_command(CONSOLE_READ_ADC));assert(console_led_level(CONSOLE_LED_ON,false,&level)&&level);assert(console_led_level(CONSOLE_LED_ON,true,&level)&&!level);assert(!console_led_level(CONSOLE_READ_ADC,false,&level));assert(console_parse("LED")==CONSOLE_INVALID);
    const uint8_t command[]={'L','E','D',' ','O','N'}; uint8_t line[7]={0U}; sim_uart_reset(); sim_gpio_reset(); assert(sim_uart_inject_rx(command,sizeof command)==SIM_UART_OK); for(size_t index=0U;index<sizeof command;++index)assert(sim_uart_read(&line[index])==SIM_UART_OK); assert(console_parse((const char *)line)==CONSOLE_LED_ON); assert(sim_gpio_configure(5U,SIM_GPIO_OUTPUT)==SIM_GPIO_OK); assert(sim_gpio_write(5U,SIM_GPIO_HIGH)==SIM_GPIO_OK); enum sim_gpio_level led=SIM_GPIO_LOW; assert(sim_gpio_read(5U,&led)==SIM_GPIO_OK&&led==SIM_GPIO_HIGH);
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
