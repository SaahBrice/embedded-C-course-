#include "board_pins.h"
#include "board_stm32_hal.h"
#include "stm32c0xx_hal.h"

#define BOARD_GPIO_PIN(number) ((uint16_t)(UINT32_C(1) << (number)))

UART_HandleTypeDef huart2;

int board_stm32_init(void) {
    GPIO_InitTypeDef gpio = {0};

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_USART2_CLK_ENABLE();

    HAL_GPIO_WritePin(GPIOA, BOARD_GPIO_PIN(BOARD_LED_PIN), GPIO_PIN_RESET);
    gpio.Pin = BOARD_GPIO_PIN(BOARD_LED_PIN);
    gpio.Mode = GPIO_MODE_OUTPUT_PP;
    gpio.Pull = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &gpio);

    gpio.Pin = BOARD_GPIO_PIN(BOARD_BUTTON_PIN);
    gpio.Mode = GPIO_MODE_INPUT;
    gpio.Pull = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;
    gpio.Alternate = 0U;
    HAL_GPIO_Init(GPIOC, &gpio);

    gpio.Pin = BOARD_GPIO_PIN(BOARD_VCP_TX_PIN) | BOARD_GPIO_PIN(BOARD_VCP_RX_PIN);
    gpio.Mode = GPIO_MODE_AF_PP;
    gpio.Pull = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;
    gpio.Alternate = GPIO_AF1_USART2;
    HAL_GPIO_Init(GPIOA, &gpio);

    huart2.Instance = USART2;
    huart2.Init.BaudRate = 115200U;
    huart2.Init.WordLength = UART_WORDLENGTH_8B;
    huart2.Init.StopBits = UART_STOPBITS_1;
    huart2.Init.Parity = UART_PARITY_NONE;
    huart2.Init.Mode = UART_MODE_TX_RX;
    huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart2.Init.OverSampling = UART_OVERSAMPLING_16;
    huart2.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
    huart2.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
    return HAL_UART_Init(&huart2) == HAL_OK;
}
