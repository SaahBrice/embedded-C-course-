/* Mission: Capstone: Serialize Deterministically */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool record_serialize(const struct serial_record *record,uint8_t *bytes,size_t capacity){if(record==NULL||bytes==NULL||capacity<RECORD_WIRE_SIZE)return false;bytes[0]=1U;uint32_t t=record->timestamp_ms;uint32_t v=(uint32_t)record->value;for(unsigned i=0U;i<4U;++i){bytes[1U+i]=(uint8_t)(t>>(8U*i));bytes[5U+i]=(uint8_t)(v>>(8U*i));}return true;}
