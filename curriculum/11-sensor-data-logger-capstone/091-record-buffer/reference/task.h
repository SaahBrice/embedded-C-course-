#ifndef LEARN_RECORD_BUFFER_TASK_H
#define LEARN_RECORD_BUFFER_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define RECORD_RING_CAPACITY 3U
struct log_record { uint32_t timestamp; int32_t value; };
struct record_ring { struct log_record data[RECORD_RING_CAPACITY]; size_t head,tail,count; };
bool record_ring_push(struct record_ring *ring, struct log_record record);
bool record_ring_pop(struct record_ring *ring, struct log_record *out_record);

#endif
