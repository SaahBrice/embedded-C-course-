#ifndef LEARN_PACKET_PARSER_RELEASE_TASK_H
#define LEARN_PACKET_PARSER_RELEASE_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

struct parsed_packet { uint8_t kind; uint16_t value; };
bool packet_header_valid(const uint8_t *bytes, size_t length);
bool packet_decode_value(const uint8_t *bytes, size_t length, uint16_t *out_value);
bool packet_parse(const uint8_t *bytes, size_t length, struct parsed_packet *out_packet);

#endif
