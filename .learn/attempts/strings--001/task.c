#include "task.h"


bool buffer_append(char *destination, size_t capacity, const char *suffix) {
    if(destination==NULL || suffix == NULL || capacity ==0) return false;
    
    size_t used = 0U;
    while (used < capacity && destination[used] != '\0')
    {
        ++used;
    }
    if (used == capacity) return false;
    const size_t added = strlen(suffix);
    if (added >= capacity - used )
    {
        return false;
    }
    memcpy(destination + used, suffix, added + 1U); 
    return true;
    
    
}
