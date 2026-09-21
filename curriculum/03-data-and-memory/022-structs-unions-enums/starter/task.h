#ifndef LEARN_STRUCTS_UNIONS_ENUMS_TASK_H
#define LEARN_STRUCTS_UNIONS_ENUMS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

enum packet_kind { PACKET_TEMPERATURE, PACKET_HUMIDITY };
struct sensor_packet { enum packet_kind kind; union { int16_t temperature_centi_c; uint16_t humidity_centi_percent; } payload; };
bool packet_value(const struct sensor_packet *packet, int32_t *out_value);

#endif
