#include "pico/cyw43_arch.h"
#include "pico/stdlib.h"

int main(void) {
  if (cyw43_arch_init()) {
    return -1;
  }

  while (true) {
    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 1);
    sleep_ms(100);

    cyw43_arch_gpio_put(CYW43_WL_GPIO_LED_PIN, 0);
    sleep_ms(900);
  }
}