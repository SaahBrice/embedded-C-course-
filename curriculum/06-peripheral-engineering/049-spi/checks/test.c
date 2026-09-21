#include "task.h"
#include "sim_spi.h"

#include <assert.h>
#include <limits.h>
#include <string.h>




int main(void) {
    uint8_t tx[2]={0U}; size_t n=0U; assert(spi_build_read(0x12U,tx,2U,&n)&&n==2U&&tx[0]==0x92U&&tx[1]==0xffU); assert(!spi_build_read(0x80U,tx,2U,&n)); assert(!spi_build_read(1U,tx,1U,&n));
    uint8_t built[2]={0U},rx_bytes[2]={0U}; size_t built_count=0U; const uint8_t reply[]={0U,UINT8_C(0x5a)}; sim_spi_reset(); assert(spi_build_read(UINT8_C(0x12),built,sizeof built,&built_count)); assert(sim_spi_set_response(reply,sizeof reply)==SIM_SPI_OK); assert(sim_spi_transfer(built,rx_bytes,built_count)==SIM_SPI_NOT_SELECTED); sim_spi_select(true); assert(sim_spi_transfer(built,rx_bytes,built_count)==SIM_SPI_OK&&rx_bytes[1]==UINT8_C(0x5a));
    return 0;
}
