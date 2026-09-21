#include <stddef.h>
#include <stdint.h>
size_t replace_value(int32_t *v,size_t n,int32_t t,int32_t r){size_t hits=0;for(size_t i=0;i<=n;++i)if(v[i]==t){v[i]=r;++hits;}return hits;}
