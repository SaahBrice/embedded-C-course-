#include "board_pins.h"
#include "board_stm32_hal.h"
#include "stm32c0xx_hal.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

GPIO_TypeDef fake_gpio_a = {1U};
GPIO_TypeDef fake_gpio_c = {2U};
unsigned fake_usart2;

static GPIO_TypeDef *observed_port;
static uint16_t observed_pin;
static GPIO_PinState observed_state;
static GPIO_PinState fake_button_state;
static GPIO_TypeDef *observed_init_ports[3];
static GPIO_InitTypeDef observed_init_configurations[3];
static size_t observed_init_count;
static UART_HandleTypeDef *observed_uart;
static uint8_t observed_bytes[32];
static uint16_t observed_length;
static uint32_t observed_timeout;
static unsigned observed_transmit_count;
static HAL_StatusTypeDef fake_uart_init_status;
static HAL_StatusTypeDef fake_uart_transmit_status;
static unsigned gpioa_clock_count;
static unsigned gpioc_clock_count;
static unsigned usart2_clock_count;

void fake_enable_gpioa_clock(void) { ++gpioa_clock_count; }
void fake_enable_gpioc_clock(void) { ++gpioc_clock_count; }
void fake_enable_usart2_clock(void) { ++usart2_clock_count; }

void HAL_GPIO_WritePin(GPIO_TypeDef *port, uint16_t pin, GPIO_PinState state) {
    observed_port = port;
    observed_pin = pin;
    observed_state = state;
}

GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef *port, uint16_t pin) {
    observed_port = port;
    observed_pin = pin;
    return fake_button_state;
}

void HAL_GPIO_Init(GPIO_TypeDef *port, const GPIO_InitTypeDef *configuration) {
    assert(observed_init_count < 3U);
    observed_init_ports[observed_init_count] = port;
    observed_init_configurations[observed_init_count] = *configuration;
    ++observed_init_count;
}

HAL_StatusTypeDef HAL_UART_Init(UART_HandleTypeDef *uart) {
    observed_uart = uart;
    return fake_uart_init_status;
}

HAL_StatusTypeDef HAL_UART_Transmit(
    UART_HandleTypeDef *uart, const uint8_t *bytes, uint16_t length, uint32_t timeout
) {
    ++observed_transmit_count;
    observed_uart = uart;
    observed_length = length;
    observed_timeout = timeout;
    memcpy(observed_bytes, bytes, length);
    return fake_uart_transmit_status;
}

int main(void) {
    fake_uart_init_status = HAL_OK;
    assert(board_stm32_init());
    assert(gpioa_clock_count == 1U);
    assert(gpioc_clock_count == 1U);
    assert(usart2_clock_count == 1U);
    assert(observed_init_count == 3U);
    assert(observed_init_ports[0] == GPIOA);
    assert(observed_init_configurations[0].Pin == GPIO_PIN_5);
    assert(observed_init_configurations[0].Mode == GPIO_MODE_OUTPUT_PP);
    assert(observed_init_ports[1] == GPIOC);
    assert(observed_init_configurations[1].Pin == GPIO_PIN_13);
    assert(observed_init_configurations[1].Mode == GPIO_MODE_INPUT);
    assert(observed_init_ports[2] == GPIOA);
    assert(observed_init_configurations[2].Pin == (GPIO_PIN_2 | GPIO_PIN_3));
    assert(observed_init_configurations[2].Mode == GPIO_MODE_AF_PP);
    assert(observed_init_configurations[2].Alternate == GPIO_AF1_USART2);
    assert(observed_uart == &huart2);
    assert(huart2.Instance == USART2);
    assert(huart2.Init.BaudRate == UINT32_C(115200));
    assert(huart2.Init.WordLength == UART_WORDLENGTH_8B);
    assert(huart2.Init.StopBits == UART_STOPBITS_1);
    assert(huart2.Init.Parity == UART_PARITY_NONE);
    assert(huart2.Init.Mode == UART_MODE_TX_RX);

    board_stm32_set_led(NULL, 1);
    assert(observed_port == GPIOA);
    assert(observed_pin == (uint16_t)(UINT32_C(1) << BOARD_LED_PIN));
    assert(observed_state == GPIO_PIN_SET);
    board_stm32_set_led(NULL, 0);
    assert(observed_state == GPIO_PIN_RESET);

    static const char message[] = "ready";
    fake_button_state = GPIO_PIN_RESET;
    assert(board_stm32_button_pressed(NULL));
    assert(observed_port == GPIOC);
    assert(observed_pin == GPIO_PIN_13);
    fake_button_state = GPIO_PIN_SET;
    assert(!board_stm32_button_pressed(NULL));

    fake_uart_transmit_status = HAL_OK;
    assert(board_stm32_write_uart(NULL, message, strlen(message)));
    assert(observed_uart == &huart2);
    assert(observed_length == strlen(message));
    assert(observed_timeout == 100U);
    assert(memcmp(observed_bytes, message, observed_length) == 0);

    const unsigned valid_transmit_count = observed_transmit_count;
    assert(!board_stm32_write_uart(NULL, NULL, 0U));
    assert(!board_stm32_write_uart(NULL, message, (size_t)UINT16_MAX + 1U));
    assert(observed_transmit_count == valid_transmit_count);
    fake_uart_transmit_status = HAL_ERROR;
    assert(!board_stm32_write_uart(NULL, message, strlen(message)));
    fake_uart_transmit_status = HAL_BUSY;
    assert(!board_stm32_write_uart(NULL, message, strlen(message)));
    fake_uart_transmit_status = HAL_TIMEOUT;
    assert(!board_stm32_write_uart(NULL, message, strlen(message)));

    observed_init_count = 0U;
    fake_uart_init_status = HAL_ERROR;
    assert(!board_stm32_init());

    puts("stm32 target adapter contract: passed");
    return 0;
}
