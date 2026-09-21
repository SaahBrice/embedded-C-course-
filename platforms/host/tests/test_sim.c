#include "sim_adc.h"
#include "sim_gpio.h"
#include "sim_i2c.h"
#include "sim_interrupt.h"
#include "sim_mmio.h"
#include "sim_pwm.h"
#include "sim_spi.h"
#include "sim_timer.h"
#include "sim_uart.h"

#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static void test_gpio(void) {
    enum sim_gpio_level level = SIM_GPIO_LOW;
    sim_gpio_reset();
    assert(sim_gpio_write(2U, SIM_GPIO_HIGH) == SIM_GPIO_MODE);
    assert(sim_gpio_configure(2U, SIM_GPIO_OUTPUT) == SIM_GPIO_OK);
    assert(sim_gpio_write(2U, SIM_GPIO_HIGH) == SIM_GPIO_OK);
    assert(sim_gpio_read(2U, &level) == SIM_GPIO_OK);
    assert(level == SIM_GPIO_HIGH);
    assert(sim_gpio_configure(SIM_GPIO_PIN_COUNT, SIM_GPIO_OUTPUT) == SIM_GPIO_RANGE);
    assert(sim_gpio_event_count() == 2U);
}

static void test_uart(void) {
    const uint8_t input[] = {'O', 'K'};
    uint8_t byte = 0U;
    uint8_t output[3] = {0U};
    sim_uart_reset();
    assert(sim_uart_inject_rx(input, sizeof input) == SIM_UART_OK);
    assert(sim_uart_rx_pending() == 2U);
    assert(sim_uart_read(&byte) == SIM_UART_OK && byte == 'O');
    assert(sim_uart_write(input, sizeof input) == SIM_UART_OK);
    assert(sim_uart_drain_tx(output, sizeof output) == 2U);
    assert(memcmp(input, output, sizeof input) == 0);
    assert(sim_uart_tx_pending() == 0U);
}

static void test_timer(void) {
    sim_timer_reset(UINT32_MAX - 2U);
    sim_timer_advance(5U);
    assert(sim_timer_now() == 2U);
    assert(sim_timer_elapsed(UINT32_MAX - 2U) == 5U);
    assert(sim_timer_deadline_reached(1U));
    assert(!sim_timer_deadline_reached(10U));
}

static void test_adc(void) {
    uint16_t value = 0U;
    sim_adc_reset();
    assert(sim_adc_set(3U, 2048U) == SIM_ADC_OK);
    assert(sim_adc_read(3U, &value) == SIM_ADC_OK && value == 2048U);
    assert(sim_adc_set(3U, 4096U) == SIM_ADC_RANGE);
    assert(sim_adc_read(SIM_ADC_CHANNEL_COUNT, &value) == SIM_ADC_CHANNEL);
}

static void test_mmio(void) {
    uint32_t value = 0U;
    sim_mmio_reset();
    assert(sim_mmio_write(3U, UINT32_C(0xffff0000)) == SIM_MMIO_OK);
    assert(sim_mmio_update(3U, UINT32_C(0x00ff0000), UINT32_C(0x00550000)) == SIM_MMIO_OK);
    assert(sim_mmio_read(3U, &value) == SIM_MMIO_OK && value == UINT32_C(0xff550000));
    assert(sim_mmio_read_count() == 2U && sim_mmio_write_count() == 2U);
    assert(sim_mmio_read(SIM_MMIO_REGISTER_COUNT, &value) == SIM_MMIO_RANGE);
}

static void capture_interrupt(void *context, uint32_t event) { *(uint32_t *)context = event; }
static void test_interrupt(void) {
    uint32_t event = 0U;
    sim_interrupt_reset();
    assert(sim_interrupt_register(2U, capture_interrupt, &event) == SIM_INTERRUPT_OK);
    assert(sim_interrupt_trigger(2U, 17U) == SIM_INTERRUPT_DISABLED);
    assert(sim_interrupt_enable(2U, true) == SIM_INTERRUPT_OK);
    assert(sim_interrupt_trigger(2U, 17U) == SIM_INTERRUPT_OK && event == 17U);
    assert(sim_interrupt_dispatch_count() == 1U);
}

static void test_pwm(void) {
    uint32_t period = 0U, compare = 0U;
    sim_pwm_reset();
    assert(sim_pwm_configure(1U, 1000U, 250U) == SIM_PWM_OK);
    assert(sim_pwm_observe(1U, &period, &compare) == SIM_PWM_OK);
    assert(period == 1000U && compare == 250U && sim_pwm_update_count() == 1U);
    assert(sim_pwm_configure(1U, 10U, 11U) == SIM_PWM_ARGUMENT);
}

static void test_spi(void) {
    const uint8_t response[] = {0U, UINT8_C(0x5a)};
    const uint8_t tx[] = {UINT8_C(0x92), UINT8_C(0xff)};
    uint8_t rx[2] = {0U}, observed[2] = {0U};
    sim_spi_reset();
    assert(sim_spi_set_response(response, sizeof response) == SIM_SPI_OK);
    assert(sim_spi_transfer(tx, rx, sizeof tx) == SIM_SPI_NOT_SELECTED);
    sim_spi_select(true);
    assert(sim_spi_transfer(tx, rx, sizeof tx) == SIM_SPI_OK && rx[1] == UINT8_C(0x5a));
    sim_spi_select(false);
    assert(sim_spi_last_tx(observed, sizeof observed) == 2U && memcmp(observed, tx, sizeof tx) == 0);
    assert(sim_spi_transaction_count() == 1U);
}

static void test_i2c(void) {
    const uint8_t registers[] = {UINT8_C(0x11), UINT8_C(0x42)};
    uint8_t value = 0U;
    sim_i2c_reset();
    assert(sim_i2c_attach(UINT8_C(0x48), registers, sizeof registers) == SIM_I2C_OK);
    assert(sim_i2c_read_register(UINT8_C(0x48), 1U, &value) == SIM_I2C_OK && value == UINT8_C(0x42));
    sim_i2c_fail_next(SIM_I2C_NACK);
    assert(sim_i2c_read_register(UINT8_C(0x48), 1U, &value) == SIM_I2C_NACK);
    assert(sim_i2c_read_register(UINT8_C(0x49), 1U, &value) == SIM_I2C_ADDRESS);
    assert(sim_i2c_transaction_count() == 3U);
}

int main(void) {
    test_gpio();
    test_uart();
    test_timer();
    test_adc();
    test_mmio();
    test_interrupt();
    test_pwm();
    test_spi();
    test_i2c();
    puts("host simulation: 9 suites passed");
    return 0;
}
