#include "task.h"


bool temperature_fits_i16(int32_t milli_celcius){
    return (milli_celcius >= INT16_MIN && milli_celcius <= INT16_MAX);
}
/* TODO — Choose Integer Types Deliberately: implement the declared interface.
 * Contract to prove: The range check proves whether a signed 32-bit measurement can be represented by int16_t before narrowing.
 */
