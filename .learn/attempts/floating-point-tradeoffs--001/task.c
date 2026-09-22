#include "task.h"


bool volts_to_millivolts(double volts, uint32_t *out_millivolts){
    if(out_millivolts==NULL || volts<0.0 || volts>65.535 || !isfinite(volts)) return false;
    *out_millivolts=(uint32_t)((volts*1000) + 0.5);
    return true;
}
/* TODO — Measure Floating-Point Trade-offs: implement the declared interface.
 * Contract to prove: Finite nonnegative volts in the documented range are rounded to integer millivolts; invalid ranges are rejected.
 */
