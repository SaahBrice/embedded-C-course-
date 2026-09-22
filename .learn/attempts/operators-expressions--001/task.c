#include "task.h"


uint32_t status_bits_update(uint32_t status, uint32_t set_mask, uint32_t clear_mask) { 
    return (status | set_mask) & ~clear_mask; 
}

/* TODO — Control Expression Evaluation: implement the declared interface.
 * Contract to prove: The expression sets requested bits, clears requested bits last, and contains no hidden side effects.
 */
