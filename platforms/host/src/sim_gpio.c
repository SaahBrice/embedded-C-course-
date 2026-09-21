#include "sim_gpio.h"

struct gpio_pin {
    enum sim_gpio_mode mode;
    enum sim_gpio_level level;
};

static struct gpio_pin pins[SIM_GPIO_PIN_COUNT];
static size_t event_count;

static int valid_level(enum sim_gpio_level level) {
    return level == SIM_GPIO_LOW || level == SIM_GPIO_HIGH;
}

void sim_gpio_reset(void) {
    for (size_t index = 0U; index < SIM_GPIO_PIN_COUNT; ++index) {
        pins[index].mode = SIM_GPIO_INPUT;
        pins[index].level = SIM_GPIO_LOW;
    }
    event_count = 0U;
}

enum sim_gpio_result sim_gpio_configure(size_t pin, enum sim_gpio_mode mode) {
    if (pin >= SIM_GPIO_PIN_COUNT) return SIM_GPIO_RANGE;
    if (mode != SIM_GPIO_INPUT && mode != SIM_GPIO_OUTPUT) return SIM_GPIO_ARGUMENT;
    pins[pin].mode = mode;
    event_count++;
    return SIM_GPIO_OK;
}

enum sim_gpio_result sim_gpio_write(size_t pin, enum sim_gpio_level level) {
    if (pin >= SIM_GPIO_PIN_COUNT) return SIM_GPIO_RANGE;
    if (!valid_level(level)) return SIM_GPIO_ARGUMENT;
    if (pins[pin].mode != SIM_GPIO_OUTPUT) return SIM_GPIO_MODE;
    pins[pin].level = level;
    event_count++;
    return SIM_GPIO_OK;
}

enum sim_gpio_result sim_gpio_read(size_t pin, enum sim_gpio_level *level) {
    if (level == NULL) return SIM_GPIO_ARGUMENT;
    if (pin >= SIM_GPIO_PIN_COUNT) return SIM_GPIO_RANGE;
    *level = pins[pin].level;
    return SIM_GPIO_OK;
}

enum sim_gpio_result sim_gpio_inject_input(size_t pin, enum sim_gpio_level level) {
    if (pin >= SIM_GPIO_PIN_COUNT) return SIM_GPIO_RANGE;
    if (!valid_level(level)) return SIM_GPIO_ARGUMENT;
    if (pins[pin].mode != SIM_GPIO_INPUT) return SIM_GPIO_MODE;
    pins[pin].level = level;
    event_count++;
    return SIM_GPIO_OK;
}

size_t sim_gpio_event_count(void) { return event_count; }
