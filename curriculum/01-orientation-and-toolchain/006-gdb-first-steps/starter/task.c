#include "task.h"
bool sample_sum(const int16_t *s,size_t n,int32_t *out){if(s==NULL||out==NULL)return false;int32_t total=0;for(size_t i=0U;i<=n;++i)total+=s[i];*out=total;return true;}
/* Debug the bound, then implement the three missing interfaces. */
