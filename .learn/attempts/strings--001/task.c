#include "task.h"
bool buffer_append(char *destination, size_t capacity, const char *suffix) {
    (void)capacity; strcat(destination, suffix); return true; /* unsafe: repair this boundary */
}
