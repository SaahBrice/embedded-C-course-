/* Mission: Connect Firmware to Electronics */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool led_output_level(bool active_low,bool led_on){return active_low?!led_on:led_on;}
