#include "task.h"
#include "sim_spi.h"

#include <limits.h>
#include <stdio.h>
#include <string.h>



static bool visible_return_spi_build_read(const char *call, bool value) { printf("Call and inputs: %s\n  Actual return: %s\n", call, value ? "true" : "false"); return value; }
#define spi_build_read(...) visible_return_spi_build_read("spi_build_read(" #__VA_ARGS__ ")", (spi_build_read)(__VA_ARGS__))

#define VISIBLE_CASE_COUNT 7

static unsigned visible_case_number;
static unsigned visible_failures;

static void visible_check(int passed, const char *expression) {
    printf("Case %u\n  Expected condition: %s\n  Observed condition: %s\n  Result: %s\n",
           visible_case_number, expression, passed ? "true" : "false",
           passed ? "PASS" : "FAIL");
    if (!passed) ++visible_failures;
}

#define assert(expression) do {     ++visible_case_number;     visible_check(!!(expression), #expression); } while (0)

int main(void) {
    uint8_t tx[2]={0U}; size_t n=0U; assert(spi_build_read(0x12U,tx,2U,&n)&&n==2U&&tx[0]==0x92U&&tx[1]==0xffU); assert(!spi_build_read(0x80U,tx,2U,&n)); assert(!spi_build_read(1U,tx,1U,&n));
    uint8_t built[2]={0U},rx_bytes[2]={0U}; size_t built_count=0U; const uint8_t reply[]={0U,UINT8_C(0x5a)}; sim_spi_reset(); assert(spi_build_read(UINT8_C(0x12),built,sizeof built,&built_count)); assert(sim_spi_set_response(reply,sizeof reply)==SIM_SPI_OK); assert(sim_spi_transfer(built,rx_bytes,built_count)==SIM_SPI_NOT_SELECTED); sim_spi_select(true); assert(sim_spi_transfer(built,rx_bytes,built_count)==SIM_SPI_OK&&rx_bytes[1]==UINT8_C(0x5a));
    printf("Visible run: %u cases checked; %u failed.\n",
           VISIBLE_CASE_COUNT, visible_failures);
    return visible_failures == 0U ? 0 : 1;
}
