#ifndef RECORD_QUEUE_INTERNAL_H
#define RECORD_QUEUE_INTERNAL_H

#include "record_queue.h"

struct record_queue_state {
    struct record_queue_record records[RECORD_QUEUE_CAPACITY];
    size_t head;
    size_t tail;
    size_t count;
};

_Static_assert(
    sizeof(struct record_queue_state) <= RECORD_QUEUE_PRIVATE_BYTES,
    "RECORD_QUEUE_PRIVATE_BYTES is too small for the private state"
);

#endif
