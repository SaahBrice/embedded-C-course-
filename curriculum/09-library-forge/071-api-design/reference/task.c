/* Mission: Design a Stable Library API */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool counter_add_bounded(unsigned current,unsigned increment,unsigned limit,unsigned *out_value){if(out_value==NULL||current>limit||increment>limit-current)return false;*out_value=current+increment;return true;}
