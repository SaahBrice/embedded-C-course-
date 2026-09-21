/* Mission: Validate Untrusted Data */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool frame_payload_length(const uint8_t *frame,size_t received,size_t *out_length){if(frame==NULL||out_length==NULL||received<2U)return false;const size_t length=frame[1];if(length>received-2U)return false;*out_length=length;return true;}
