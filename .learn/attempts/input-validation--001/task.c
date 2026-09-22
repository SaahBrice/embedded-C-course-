#include "task.h"


bool parse_u16(const char *text, uint16_t *out_value){
    if(text == NULL || out_value == NULL || text[0] == '\0' || text[0]=='-') return false;

    errno =0;
    char *end=NULL;
    const unsigned long parsed = strtoul(text, &end, 10);
    if(errno != 0 || end == text || *end != '\0' || parsed > UINT16_MAX) return false;
    *out_value = (uint16_t)parsed; 
    return true;
}
/* TODO — Validate External Input: implement the declared interface.
 * Contract to prove: The parser accepts the complete decimal string only, checks conversion errors and range, and never accepts a negative value.
 */
