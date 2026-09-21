#include <rq.h>
#include <string.h>

int main(void) {
    if (strcmp(rq_version(), "1.0.0") != 0) return 1;
    if (rq_add(19, 23) != 42) return 2;
    return 0;
}
