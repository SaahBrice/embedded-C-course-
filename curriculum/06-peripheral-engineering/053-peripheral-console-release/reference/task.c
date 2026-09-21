/* Mission: Release: Peripheral Console */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

enum console_command console_parse(const char *line){if(line==NULL)return CONSOLE_INVALID;if(strcmp(line,"LED ON")==0)return CONSOLE_LED_ON;if(strcmp(line,"LED OFF")==0)return CONSOLE_LED_OFF;if(strcmp(line,"READ ADC")==0)return CONSOLE_READ_ADC;return CONSOLE_INVALID;}
bool console_is_led_command(enum console_command command){return command==CONSOLE_LED_ON||command==CONSOLE_LED_OFF;}
bool console_led_level(enum console_command command,bool active_low,bool *out){if(out==NULL||!console_is_led_command(command))return false;const bool on=command==CONSOLE_LED_ON;*out=active_low?!on:on;return true;}
