#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    struct sensor_packet t = {PACKET_TEMPERATURE, {.temperature_centi_c = -125}}; int32_t value = 0;
assert(packet_value(&t, &value) && value == -125); struct sensor_packet h = {PACKET_HUMIDITY, {.humidity_centi_percent = 4567U}}; assert(packet_value(&h, &value) && value == 4567); t.kind = (enum packet_kind)99; assert(!packet_value(&t, &value));
    
    return 0;
}
