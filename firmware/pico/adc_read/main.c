#include "hardware/adc.h"
#include "pico/stdlib.h"
#include <pico/time.h>
#include <stdint.h>
#include <stdio.h>

int main(void) {
  stdio_init_all();

  adc_init();
  adc_gpio_init(26);
  adc_select_input(0);

  const float conversion_factor = 3.3f / 4095.0f;

  while (true) {
    uint32_t time_ms = to_ms_since_boot(get_absolute_time());
    uint16_t raw = adc_read();
    float voltage = raw * conversion_factor;

    printf("%lu,%u,%.3f\n", (unsigned long)time_ms, raw, voltage);

    sleep_ms(50);
  }
}