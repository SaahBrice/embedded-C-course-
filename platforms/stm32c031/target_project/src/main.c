#include "app.h"
#include "board_stm32_hal.h"
#include "stm32c0xx_hal.h"

static int system_clock_configure(void) {
    RCC_OscInitTypeDef oscillator = {0};
    RCC_ClkInitTypeDef clock = {0};

    oscillator.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    oscillator.HSIState = RCC_HSI_ON;
    oscillator.HSIDiv = RCC_HSI_DIV1;
    oscillator.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    if (HAL_RCC_OscConfig(&oscillator) != HAL_OK) return 0;

    clock.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK | RCC_CLOCKTYPE_PCLK1;
    clock.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
    clock.SYSCLKDivider = RCC_SYSCLK_DIV1;
    clock.AHBCLKDivider = RCC_HCLK_DIV1;
    clock.APB1CLKDivider = RCC_APB1_DIV1;
    return HAL_RCC_ClockConfig(&clock, FLASH_LATENCY_1) == HAL_OK;
}

static void stop_on_error(void) {
    __disable_irq();
    for (;;) {
    }
}

int main(void) {
    struct app application;
    const struct app_port port = {
        NULL,
        board_stm32_set_led,
        board_stm32_write_uart,
    };

    if (HAL_Init() != HAL_OK) stop_on_error();
    if (!system_clock_configure()) stop_on_error();
    if (!board_stm32_init()) stop_on_error();
    if (!app_init(&application, &port, HAL_GetTick())) stop_on_error();

    for (;;) {
        app_step(&application, HAL_GetTick());
    }
}
