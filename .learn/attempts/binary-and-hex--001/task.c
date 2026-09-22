#include "task.h"

/* TODO — Decode Binary and Hexadecimal: implement the declared interface.
 * Contract to prove: The high and low four-bit nibbles exchange positions without changing any bit.
 */

 uint8_t swap_nibbles(uint8_t value){
    return (uint8_t)((value << 4) | (value >> 4));
 }