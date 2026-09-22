#include "task.h"

/* TODO — Trace Source to Executable: implement the declared interface.
 * Contract to prove: A separately declared function produces input plus one, rejects overflow, and writes output only on success.
 */

 bool linked_increment(int32_t input, int32_t *output){
    if (input == INT32_MAX || output == NULL)return false;
    *output = input +1;
    return true;
 }