#include "app.h"

#define APP_TOGGLE_PERIOD_MS UINT32_C(500)

int app_init(struct app *app, const struct app_port *port, uint32_t now_ms) {
    static const char message[] = "NUCLEO-C031C6 app ready\r\n";
    if (app == NULL || port == NULL || port->set_led == NULL || port->write_uart == NULL) return 0;
    app->port = *port;
    app->last_toggle_ms = now_ms;
    app->led_on = 0;
    app->port.set_led(app->port.context, 0);
    return app->port.write_uart(app->port.context, message, sizeof message - 1U);
}

void app_step(struct app *app, uint32_t now_ms) {
    if (app == NULL) return;
    if ((uint32_t)(now_ms - app->last_toggle_ms) < APP_TOGGLE_PERIOD_MS) return;
    app->last_toggle_ms = now_ms;
    app->led_on = !app->led_on;
    app->port.set_led(app->port.context, app->led_on);
}
