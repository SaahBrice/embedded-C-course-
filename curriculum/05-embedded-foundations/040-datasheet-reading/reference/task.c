/* Mission: Read a Peripheral Datasheet */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool datasheet_field_encode(uint32_t value,unsigned shift,uint32_t mask,uint32_t *out_bits){
    if(out_bits==NULL||shift>=32U||(mask>>shift)<value)return false;
    *out_bits=(value<<shift)&mask;return true;
}
