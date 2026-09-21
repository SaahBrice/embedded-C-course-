/* Mission: Release: Register-Level GPIO Driver */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool gpio_pin_valid(unsigned pin){return pin<16U;}
bool gpio_mode_set(uint32_t original,unsigned pin,uint32_t mode,uint32_t *out){if(out==NULL||!gpio_pin_valid(pin)||mode>3U)return false;const unsigned shift=pin*2U;const uint32_t mask=UINT32_C(3)<<shift;*out=(original&~mask)|(mode<<shift);return true;}
bool gpio_mode_matches(uint32_t value,unsigned pin,uint32_t mode){return gpio_pin_valid(pin)&&mode<=3U&&((value>>(pin*2U))&UINT32_C(3))==mode;}
