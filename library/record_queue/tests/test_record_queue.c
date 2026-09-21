#include "record_queue.h"

#include <assert.h>
#include <stdio.h>
#include <string.h>

static void test_empty(void) {
    struct record_queue queue;
    struct record_queue_record record;
    record_queue_init(&queue);
    assert(record_queue_count(&queue) == 0U);
    assert(record_queue_pop(&queue, &record) == RECORD_QUEUE_EMPTY);
}

static void test_arguments(void) {
    struct record_queue queue;
    struct record_queue_record record = {0U, 0, 0U};
    record_queue_init(&queue);
    assert(record_queue_push(NULL, &record) == RECORD_QUEUE_ARGUMENT);
    assert(record_queue_push(&queue, NULL) == RECORD_QUEUE_ARGUMENT);
    assert(record_queue_pop(NULL, &record) == RECORD_QUEUE_ARGUMENT);
    assert(record_queue_count(NULL) == 0U);
}

static void test_fifo(void) {
    struct record_queue queue;
    struct record_queue_record first = {1U, 10, 0U};
    struct record_queue_record second = {2U, 20, 1U};
    struct record_queue_record output;
    record_queue_init(&queue);
    assert(record_queue_push(&queue, &first) == RECORD_QUEUE_OK);
    assert(record_queue_push(&queue, &second) == RECORD_QUEUE_OK);
    assert(record_queue_pop(&queue, &output) == RECORD_QUEUE_OK);
    assert(output.timestamp_ms == 1U && output.value == 10);
    assert(record_queue_pop(&queue, &output) == RECORD_QUEUE_OK);
    assert(output.timestamp_ms == 2U && output.value == 20 && output.flags == 1U);
}

static void test_full_and_wrap(void) {
    struct record_queue queue;
    struct record_queue_record record = {0U, 0, 0U};
    struct record_queue_record output;
    record_queue_init(&queue);
    for (size_t index = 0U; index < RECORD_QUEUE_CAPACITY; ++index) {
        record.value = (int32_t)index;
        assert(record_queue_push(&queue, &record) == RECORD_QUEUE_OK);
    }
    assert(record_queue_push(&queue, &record) == RECORD_QUEUE_FULL);
    assert(record_queue_pop(&queue, &output) == RECORD_QUEUE_OK && output.value == 0);
    record.value = 99;
    assert(record_queue_push(&queue, &record) == RECORD_QUEUE_OK);
    for (size_t index = 1U; index < RECORD_QUEUE_CAPACITY; ++index) {
        assert(record_queue_pop(&queue, &output) == RECORD_QUEUE_OK);
        assert(output.value == (int32_t)index);
    }
    assert(record_queue_pop(&queue, &output) == RECORD_QUEUE_OK && output.value == 99);
}

static void test_version(void) {
    assert(strcmp(record_queue_version(), "1.0.0") == 0);
    assert(RECORD_QUEUE_VERSION_MAJOR == 1);
}

int main(void) {
    test_empty();
    test_arguments();
    test_fifo();
    test_full_and_wrap();
    test_version();
    puts("record_queue: 5 suites passed");
    return 0;
}
