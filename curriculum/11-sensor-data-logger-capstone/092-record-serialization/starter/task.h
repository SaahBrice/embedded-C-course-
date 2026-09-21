#ifndef LEARN_RECORD_SERIALIZATION_TASK_H
#define LEARN_RECORD_SERIALIZATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define RECORD_WIRE_SIZE 9U
struct serial_record { uint32_t timestamp_ms; int32_t value; };
bool record_serialize(const struct serial_record *record, uint8_t *bytes, size_t capacity);

#endif
