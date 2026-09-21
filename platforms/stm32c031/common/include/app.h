#ifndef LOGGER_DEMO_APP_H
#define LOGGER_DEMO_APP_H

#include <stddef.h>
#include <stdint.h>

struct app_port {
    void *context;
    void (*set_led)(void *context, int on);
    int (*write_uart)(void *context, const char *text, size_t length);
};

struct app {
    struct app_port port;
    uint32_t last_toggle_ms;
    int led_on;
};

int app_init(struct app *app, const struct app_port *port, uint32_t now_ms);
void app_step(struct app *app, uint32_t now_ms);

#endif
