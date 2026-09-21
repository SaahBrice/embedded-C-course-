CC ?= cc
AR ?= ar
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2
CPPFLAGS ?= -Iinclude

.PHONY: all test clean
all: librecord_queue.a
librecord_queue.a: record_queue.o
	$(AR) rcs $@ $^
record_queue.o: src/record_queue.c include/record_queue.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
tests/record_queue_tests: tests/test_record_queue.c librecord_queue.a
	$(CC) $(CPPFLAGS) $(CFLAGS) $< librecord_queue.a -o $@
test: tests/record_queue_tests
	./tests/record_queue_tests
clean:
	rm -f record_queue.o librecord_queue.a tests/record_queue_tests
