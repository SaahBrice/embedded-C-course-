#ifndef SIM_GPIO_H
#define SIM_GPIO_H

#include <stddef.h>

#define SIM_GPIO_PIN_COUNT 16U

enum sim_gpio_result {
    SIM_GPIO_OK = 0,
    SIM_GPIO_ARGUMENT,
    SIM_GPIO_RANGE,
    SIM_GPIO_MODE
};

enum sim_gpio_mode { SIM_GPIO_INPUT = 0, SIM_GPIO_OUTPUT };
enum sim_gpio_level { SIM_GPIO_LOW = 0, SIM_GPIO_HIGH = 1 };

void sim_gpio_reset(void);
enum sim_gpio_result sim_gpio_configure(size_t pin, enum sim_gpio_mode mode);
enum sim_gpio_result sim_gpio_write(size_t pin, enum sim_gpio_level level);
enum sim_gpio_result sim_gpio_read(size_t pin, enum sim_gpio_level *level);
enum sim_gpio_result sim_gpio_inject_input(size_t pin, enum sim_gpio_level level);
size_t sim_gpio_event_count(void);

#endif
