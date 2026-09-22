#include "task.h"


bool sample_sum(const int16_t *s,size_t n,int32_t *out){
    if(s==NULL||out==NULL)return false;
    int32_t total=0;
    for(size_t i=0U;i<n;++i)total+=s[i];
    *out=total;
    return true;
}
bool sample_minimum(const int16_t *s,size_t n,int16_t *out){
    if(s==NULL||out==NULL||n==0U)return false;
    int16_t low=s[0];
    for(size_t i=1U;i<n;++i)if(s[i]<low)low=s[i];
    *out=low;
    return true;
}
bool sample_negative_mask(const int16_t *s,size_t n,uint8_t *out){
    if(s==NULL||out==NULL||n==0U||n>8U)return false;
    uint8_t mask=0U;
    for(size_t i=0U;i<n;++i)if(s[i]<0)mask=(uint8_t)(mask|(uint8_t)(UINT8_C(1)<<i));
    *out=mask;
    return true;
}
bool sample_window_analyze(const int16_t *s,size_t n,int32_t *sum,int16_t *low,uint8_t *mask){
    if(s==NULL||n==0U||n>8U||sum==NULL||low==NULL||mask==NULL)return false;
    int32_t next_sum=0;
    int16_t next_low=0;
    uint8_t next_mask=0U;
    if(!sample_sum(s,n,&next_sum)||!sample_minimum(s,n,&next_low)||!sample_negative_mask(s,n,&next_mask))return false;
    *sum=next_sum;
    *low=next_low;
    *mask=next_mask;
    return true;
}
