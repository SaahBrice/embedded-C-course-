#include "record_queue.h"
#include "record_queue_internal.h"

#include <string.h>

static void state_load(const struct record_queue *queue, struct record_queue_state *state) {
    memcpy(state, queue->private_storage.bytes, sizeof *state);
}

static void state_store(struct record_queue *queue, const struct record_queue_state *state) {
    memcpy(queue->private_storage.bytes, state, sizeof *state);
}

void record_queue_init(struct record_queue *queue) {
    if (queue != NULL) memset(queue, 0, sizeof *queue);
}

enum record_queue_status record_queue_push(
    struct record_queue *queue,
    const struct record_queue_record *record
) {
    if (queue == NULL || record == NULL) return RECORD_QUEUE_ARGUMENT;
    struct record_queue_state state;
    state_load(queue, &state);
    if (state.count >= RECORD_QUEUE_CAPACITY) return RECORD_QUEUE_FULL;
    state.records[state.head] = *record;
    state.head = (state.head + 1U) % RECORD_QUEUE_CAPACITY;
    state.count++;
    state_store(queue, &state);
    return RECORD_QUEUE_OK;
}

enum record_queue_status record_queue_pop(
    struct record_queue *queue,
    struct record_queue_record *record
) {
    if (queue == NULL || record == NULL) return RECORD_QUEUE_ARGUMENT;
    struct record_queue_state state;
    state_load(queue, &state);
    if (state.count == 0U) return RECORD_QUEUE_EMPTY;
    *record = state.records[state.tail];
    state.tail = (state.tail + 1U) % RECORD_QUEUE_CAPACITY;
    state.count--;
    state_store(queue, &state);
    return RECORD_QUEUE_OK;
}

size_t record_queue_count(const struct record_queue *queue) {
    if (queue == NULL) return 0U;
    struct record_queue_state state;
    state_load(queue, &state);
    return state.count;
}

const char *record_queue_version(void) { return "1.0.0"; }
