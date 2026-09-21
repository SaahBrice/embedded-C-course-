CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2
RECORD_QUEUE_ROOT ?= ../../library/record_queue

.PHONY: all test clean
all: record_queue_consumer
record_queue_consumer: main.c $(RECORD_QUEUE_ROOT)/src/record_queue.c
	$(CC) $(CFLAGS) -I$(RECORD_QUEUE_ROOT)/include $^ -o $@
test: record_queue_consumer
	./record_queue_consumer
clean:
	rm -f record_queue_consumer
