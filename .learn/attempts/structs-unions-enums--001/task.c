#include "task.h"

bool packet_value(const struct sensor_packet *packet, int32_t *out_value){
    if (out_value == NULL || packet == NULL) return false;

    switch (packet->kind){
    case PACKET_HUMIDITY:
        *out_value = (uint32_t)packet->payload.humidity_centi_percent;
        break;
    case PACKET_TEMPERATURE:
        *out_value = (uint32_t)packet->payload.temperature_centi_c;
        break;
    default:
        return false;
    }

    return true;
}