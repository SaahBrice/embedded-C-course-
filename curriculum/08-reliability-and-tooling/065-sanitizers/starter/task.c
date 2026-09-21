#include "task.h"
bool copy_samples(int16_t *destination, size_t capacity, const int16_t *source, size_t count) { (void)capacity; for(size_t i=0U;i<=count;++i) destination[i]=source[i]; return true; }
