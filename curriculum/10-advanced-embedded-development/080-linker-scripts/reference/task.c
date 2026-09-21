/* Mission: Read a Linker Script */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool region_contains(uint32_t origin,uint32_t length,uint32_t address,uint32_t size){return length<=UINT32_MAX-origin&&address>=origin&&size<=length&&(address-origin)<=length-size;}
