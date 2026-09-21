/* Mission: Decode Binary and Hexadecimal */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint8_t swap_nibbles(uint8_t value) { return (uint8_t)((value << 4U) | (value >> 4U)); }
