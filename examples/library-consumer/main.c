#include <record_queue.h>

#include <stdio.h>

int main(void) {
    struct record_queue queue;
    const struct record_queue_record input = {100U, 42, 0U};
    struct record_queue_record output;
    record_queue_init(&queue);
    if (record_queue_push(&queue, &input) != RECORD_QUEUE_OK ||
        record_queue_pop(&queue, &output) != RECORD_QUEUE_OK) {
        return 1;
    }
    printf("record_queue %s: value=%ld\n", record_queue_version(), (long)output.value);
    return 0;
}
