CC ?= cc
AR ?= ar
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -Werror -O2
PREFIX ?= /usr/local
.PHONY: all clean install
all: librq.a
rq.o: rq.c rq.h
	$(CC) $(CFLAGS) -c rq.c -o rq.o
librq.a: rq.o
	$(AR) rcs $@ $^
install: librq.a rq.h
	mkdir -p $(PREFIX)/include $(PREFIX)/lib
	cp rq.h $(PREFIX)/include/rq.h
	cp librq.a $(PREFIX)/lib/librq.a
clean:
	rm -f rq.o librq.a
