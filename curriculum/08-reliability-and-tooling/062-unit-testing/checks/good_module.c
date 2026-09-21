#include "task.h"
int16_t median3(int16_t a,int16_t b,int16_t c){if(a>b){int16_t t=a;a=b;b=t;}if(b>c){int16_t t=b;b=c;c=t;}if(a>b){int16_t t=a;a=b;b=t;}return b;}
