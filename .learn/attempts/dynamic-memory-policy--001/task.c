#include "task.h"

bool fixed_pool_acquire(bool *used, size_t capacity, size_t *out_index){
    if (used == NULL || out_index == NULL) return false;
    //if (capacity > SIZE_MAX/sizeof(*used)) return false;

    for (size_t i = 0; i < capacity; i++){
        if (!used[i]){
            used[i] = true;
            *out_index = i;
            return true;
        }
    }
    return false;
}