CC ?= cc
AR ?= ar
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O0 -g
CPPFLAGS ?= -Iinclude
SOURCES := $(wildcard src/*.c)
OBJECTS := $(SOURCES:.c=.o)

.PHONY: all test clean
all: liblearnsim.a
liblearnsim.a: $(OBJECTS)
	$(AR) rcs $@ $^
src/%.o: src/%.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@
tests/test_sim: tests/test_sim.c liblearnsim.a
	$(CC) $(CPPFLAGS) $(CFLAGS) $< liblearnsim.a -o $@
test: tests/test_sim
	@status=0; ./tests/test_sim || status=$$?; $(RM) $(OBJECTS) liblearnsim.a tests/test_sim; exit $$status
clean:
	rm -f $(OBJECTS) liblearnsim.a tests/test_sim
