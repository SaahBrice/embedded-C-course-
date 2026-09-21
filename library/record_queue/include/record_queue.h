#ifndef RECORD_QUEUE_H
#define RECORD_QUEUE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define RECORD_QUEUE_CAPACITY 8U
#define RECORD_QUEUE_PRIVATE_BYTES 160U
#define RECORD_QUEUE_VERSION_MAJOR 1
#define RECORD_QUEUE_VERSION_MINOR 0
#define RECORD_QUEUE_VERSION_PATCH 0

struct record_queue_record {
    uint32_t timestamp_ms;
    int32_t value;
    uint16_t flags;
};

struct record_queue {
    union {
        max_align_t alignment;
        unsigned char bytes[RECORD_QUEUE_PRIVATE_BYTES];
    } private_storage;
};

enum record_queue_status {
    RECORD_QUEUE_OK = 0,
    RECORD_QUEUE_ARGUMENT,
    RECORD_QUEUE_FULL,
    RECORD_QUEUE_EMPTY
};

void record_queue_init(struct record_queue *queue);
enum record_queue_status record_queue_push(
    struct record_queue *queue,
    const struct record_queue_record *record
);
enum record_queue_status record_queue_pop(
    struct record_queue *queue,
    struct record_queue_record *record
);
size_t record_queue_count(const struct record_queue *queue);
const char *record_queue_version(void);

#ifdef __cplusplus
}
#endif

#endif
