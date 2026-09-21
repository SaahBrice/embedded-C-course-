/* Mission: Release: Portable CRC Module */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

uint8_t crc8_update(uint8_t crc,uint8_t byte){crc^=byte;for(unsigned bit=0U;bit<8U;++bit)crc=(uint8_t)((crc&0x80U)?(uint8_t)(crc<<1U)^0x07U:(uint8_t)(crc<<1U));return crc;}
uint8_t crc8(const uint8_t *bytes,size_t length){if(bytes==NULL&&length!=0U)return 0U;uint8_t crc=0U;for(size_t i=0U;i<length;++i)crc=crc8_update(crc,bytes[i]);return crc;}
bool crc8_verify(const uint8_t *bytes,size_t length,uint8_t expected){return(bytes!=NULL||length==0U)&&crc8(bytes,length)==expected;}
