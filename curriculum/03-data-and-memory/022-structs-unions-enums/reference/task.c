/* Mission: Model a Sensor Packet */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool packet_value(const struct sensor_packet *packet, int32_t *out_value) {
    if (packet == NULL || out_value == NULL) return false;
    switch (packet->kind) { case PACKET_TEMPERATURE: *out_value = packet->payload.temperature_centi_c; return true; case PACKET_HUMIDITY: *out_value = packet->payload.humidity_centi_percent; return true; default: return false; }
}
