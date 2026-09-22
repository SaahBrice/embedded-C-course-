#include "task.h"

/* TODO — Implement Your First Firmware Function: implement the declared interface.
 * Contract to prove: `firmware_status` returns zero only after at least one successful boot has been observed.
 */

 int firmware_status(unsigned boot_count){
    return boot_count == 0? -1:0;
 }
