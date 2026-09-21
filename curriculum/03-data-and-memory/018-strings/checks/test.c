#include "task.h"


#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    char a[8] = "AB"; assert(buffer_append(a, sizeof a, "CDE") && strcmp(a, "ABCDE") == 0);
char b[5] = "AB"; assert(!buffer_append(b, sizeof b, "CDE") && strcmp(b, "AB") == 0);
char c[1] = {0}; assert(buffer_append(c, sizeof c, "") && c[0] == '\0');
char d[3] = {'A','B','C'}; assert(!buffer_append(d, sizeof d, "x"));
    
    return 0;
}
