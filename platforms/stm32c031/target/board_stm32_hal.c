/* Drop this adapter into a NUCLEO-C031C6 STM32CubeC0 project. */
#include "app.h"
#include "board_pins.h"
#include "board_stm32_hal.h"
#include "stm32c0xx_hal.h"

#include <limits.h>

#define BOARD_GPIO_PORT_INNER(suffix) GPIO##suffix
#define BOARD_GPIO_PORT(suffix) BOARD_GPIO_PORT_INNER(suffix)
#define BOARD_GPIO_PIN(number) ((uint16_t)(UINT32_C(1) << (number)))

void board_stm32_set_led(void *context, int on) {
    (void)context;
    HAL_GPIO_WritePin(
        BOARD_GPIO_PORT(BOARD_LED_GPIO_SUFFIX),
        BOARD_GPIO_PIN(BOARD_LED_PIN),
        on ? GPIO_PIN_SET : GPIO_PIN_RESET
    );
}

int board_stm32_button_pressed(void *context) {
    (void)context;
    return HAL_GPIO_ReadPin(
        BOARD_GPIO_PORT(BOARD_BUTTON_GPIO_SUFFIX),
        BOARD_GPIO_PIN(BOARD_BUTTON_PIN)
    ) == GPIO_PIN_RESET;
}

int board_stm32_write_uart(void *context, const char *text, size_t length) {
    (void)context;
    if (text == NULL || length > UINT16_MAX) return 0;
    return HAL_UART_Transmit(
        &huart2, (const uint8_t *)text, (uint16_t)length, 100U
    ) == HAL_OK;
}

/* Integration after MX_GPIO_Init() and MX_USART2_UART_Init():
 *
 * struct app app;
 * const struct app_port port = {NULL, board_stm32_set_led, board_stm32_write_uart};
 * app_init(&app, &port, HAL_GetTick());
 * while (1) { app_step(&app, HAL_GetTick()); }
 */
