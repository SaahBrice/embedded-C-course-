CC ?= cc
AR ?= ar
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2
CPPFLAGS ?= -Iinclude

.PHONY: all test clean
all: libdata_logger.a logger_demo
data_logger.o: src/data_logger.c include/data_logger.h
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
libdata_logger.a: data_logger.o
	$(AR) rcs $@ $^
logger_demo: examples/logger_demo.c libdata_logger.a
	$(CC) $(CPPFLAGS) $(CFLAGS) $< libdata_logger.a -o $@
tests/data_logger_tests: tests/test_data_logger.c libdata_logger.a
	$(CC) $(CPPFLAGS) $(CFLAGS) $< libdata_logger.a -o $@
test: tests/data_logger_tests
	./tests/data_logger_tests
clean:
	rm -f data_logger.o libdata_logger.a logger_demo tests/data_logger_tests
