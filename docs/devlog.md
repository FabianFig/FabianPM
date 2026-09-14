# Dev Log

## 2026-09-13

### Pico W setup

Set up the Raspberry Pi Pico C/C++ SDK toolchain on Arch Linux using CMake, Ninja, and `arm-none-eabi-gcc`.
The first firmware was a basic blink program using the Pico W onboard LED. Unlike the original Pico, the Pico W LED is controlled through the CYW43 wireless chip, so the firmware uses `pico_cyw43_arch_none`.
After flashing the first version, I changed the blink timing and reflashed it to make sure I understood the edit-build-flash cycle.

### USB serial

The next test used USB CDC serial output.

The Pico appeared on Linux as:

```text
/dev/ttyACM0
```

The device belonged to the `uucp` group, so I had added my user to that group instead of accessing the serial port with `sudo`.

The firmware then printed:

```text
Hello FabianPM
```

once per second over USB.

### ADC basics

I moved on to the RP2040 ADC using GPIO26/ADC0.
The ADC is 12-bit, giving raw values from:

```text
0-4095
```

With GPIO26 floating, the readings moved around significantly.

Connecting GPIO26 to ground produced readings near zero.

Connecting GPIO26 to 3V3 produced readings near full scale.

I then built a voltage divider using two equal resistors:

```text
3V3 - R --+-- R - GND
          |                 R = resistor
        GPIO26
```

something in that configuration ^ lol

The midpoint then settled around:

```text
2050 counts
1.65 V
```

which is close to my expected half-scale value (2048).

### First data capture

I changed the ADC firmware to output:

```text
time_ms,raw_adc,voltage
```

every 50 ms, giving a target sample rate of 20 Hz.

The first saved capture contained 249 samples over approximately 12.4 seconds.
The measured average sample rate was about 19.95 Hz.
The next step is to compare the raw ADC signal with basic filtering.

### Moving-average filtering

The first captured ADC dataset was used to compare several simple moving-average filters.

The raw signal had a standard deviation of:

```text
0.0155 V
```

I then calculated moving averages over three window sizes:

```text
5 samples
10 samples
20 samples
```

At the measured sampling rate of approximately 19.95 Hz, these represent roughly:

```text
5 samples  ≈ 0.25 s
10 samples ≈ 0.50 s
20 samples ≈ 1.00 s
```

The measured standard deviations were:

```text
Raw:        0.0155 V
5-sample:   0.0065 V
10-sample:  0.0038 V
20-sample:  0.0023 V
```

he larger averaging windows visibly smoothed the signal and reduced measured variation.
And because the resistor-divider input was essentially static, this experiment mainly shows noise reduction. A changing input will needed to show the response-time penalty introduced by larger moving-average windows.
