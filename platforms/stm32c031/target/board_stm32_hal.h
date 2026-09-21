#ifndef BOARD_STM32_HAL_H
#define BOARD_STM32_HAL_H

#include <stddef.h>

#include "stm32c0xx_hal.h"

extern UART_HandleTypeDef huart2;

int board_stm32_init(void);
void board_stm32_set_led(void *context, int on);
int board_stm32_button_pressed(void *context);
int board_stm32_write_uart(void *context, const char *text, size_t length);

#endif
