#ifndef LEARN_RING_BUFFERS_TASK_H
#define LEARN_RING_BUFFERS_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define BYTE_RING_CAPACITY 4U
struct byte_ring { uint8_t data[BYTE_RING_CAPACITY]; size_t head, tail, count; };
bool byte_ring_push(struct byte_ring *ring, uint8_t value);
bool byte_ring_pop(struct byte_ring *ring, uint8_t *out_value);

#endif
