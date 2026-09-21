#ifndef TEST_STM32C0XX_HAL_H
#define TEST_STM32C0XX_HAL_H

#include <stdint.h>

typedef struct GPIO_TypeDef {
    unsigned identity;
} GPIO_TypeDef;

typedef struct UART_HandleTypeDef {
    void *Instance;
    struct {
        uint32_t BaudRate;
        uint32_t WordLength;
        uint32_t StopBits;
        uint32_t Parity;
        uint32_t Mode;
        uint32_t HwFlowCtl;
        uint32_t OverSampling;
        uint32_t OneBitSampling;
    } Init;
    struct {
        uint32_t AdvFeatureInit;
    } AdvancedInit;
} UART_HandleTypeDef;

typedef struct GPIO_InitTypeDef {
    uint32_t Pin;
    uint32_t Mode;
    uint32_t Pull;
    uint32_t Speed;
    uint32_t Alternate;
} GPIO_InitTypeDef;

typedef enum GPIO_PinState {
    GPIO_PIN_RESET = 0,
    GPIO_PIN_SET = 1,
} GPIO_PinState;

typedef enum HAL_StatusTypeDef {
    HAL_OK = 0,
    HAL_ERROR = 1,
    HAL_BUSY = 2,
    HAL_TIMEOUT = 3,
} HAL_StatusTypeDef;

extern GPIO_TypeDef fake_gpio_a;
extern GPIO_TypeDef fake_gpio_c;
extern unsigned fake_usart2;
#define GPIOA (&fake_gpio_a)
#define GPIOC (&fake_gpio_c)
#define USART2 ((void *)&fake_usart2)

#define GPIO_PIN_2 ((uint16_t)UINT16_C(0x0004))
#define GPIO_PIN_3 ((uint16_t)UINT16_C(0x0008))
#define GPIO_PIN_5 ((uint16_t)UINT16_C(0x0020))
#define GPIO_PIN_13 ((uint16_t)UINT16_C(0x2000))
#define GPIO_MODE_OUTPUT_PP UINT32_C(1)
#define GPIO_MODE_INPUT UINT32_C(2)
#define GPIO_MODE_AF_PP UINT32_C(3)
#define GPIO_NOPULL UINT32_C(0)
#define GPIO_SPEED_FREQ_LOW UINT32_C(1)
#define GPIO_AF1_USART2 UINT32_C(1)
#define UART_WORDLENGTH_8B UINT32_C(8)
#define UART_STOPBITS_1 UINT32_C(1)
#define UART_PARITY_NONE UINT32_C(0)
#define UART_MODE_TX_RX UINT32_C(3)
#define UART_HWCONTROL_NONE UINT32_C(0)
#define UART_OVERSAMPLING_16 UINT32_C(16)
#define UART_ONE_BIT_SAMPLE_DISABLE UINT32_C(0)
#define UART_ADVFEATURE_NO_INIT UINT32_C(0)

void fake_enable_gpioa_clock(void);
void fake_enable_gpioc_clock(void);
void fake_enable_usart2_clock(void);
#define __HAL_RCC_GPIOA_CLK_ENABLE() fake_enable_gpioa_clock()
#define __HAL_RCC_GPIOC_CLK_ENABLE() fake_enable_gpioc_clock()
#define __HAL_RCC_USART2_CLK_ENABLE() fake_enable_usart2_clock()

void HAL_GPIO_WritePin(GPIO_TypeDef *port, uint16_t pin, GPIO_PinState state);
GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef *port, uint16_t pin);
void HAL_GPIO_Init(GPIO_TypeDef *port, const GPIO_InitTypeDef *configuration);
HAL_StatusTypeDef HAL_UART_Init(UART_HandleTypeDef *uart);
HAL_StatusTypeDef HAL_UART_Transmit(
    UART_HandleTypeDef *uart, const uint8_t *bytes, uint16_t length, uint32_t timeout
);

#endif
