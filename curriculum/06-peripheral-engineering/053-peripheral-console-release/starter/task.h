#ifndef LEARN_PERIPHERAL_CONSOLE_RELEASE_TASK_H
#define LEARN_PERIPHERAL_CONSOLE_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum console_command { CONSOLE_INVALID, CONSOLE_LED_ON, CONSOLE_LED_OFF, CONSOLE_READ_ADC };
enum console_command console_parse(const char *line);
bool console_is_led_command(enum console_command command);
bool console_led_level(enum console_command command, bool active_low, bool *out_level);

#endif
