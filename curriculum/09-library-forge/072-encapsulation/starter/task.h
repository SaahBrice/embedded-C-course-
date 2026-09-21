#ifndef LEARN_ENCAPSULATION_TASK_H
#define LEARN_ENCAPSULATION_TASK_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct record_queue record_queue_t;
size_t record_queue_required_bytes(void);
bool record_queue_init(void *storage, size_t storage_size, record_queue_t **out_queue);
bool record_queue_push(record_queue_t *queue, uint8_t value);
bool record_queue_pop(record_queue_t *queue, uint8_t *out_value);

#endif
