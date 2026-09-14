# Experiment 003 - ADC Basics

## Objective

Read an analog voltage using the Raspberry Pi Pico W ADC, convert the raw ADC result into volts, and stream timestamped measurements over USB serial.

## Hardware

- Raspberry Pi Pico W
- Breadboard
- Two equal-value resistors
- Jumper wires
- USB connection to Arch Linux host

ADC input:

```text
GPIO26 / ADC0
```

## ADC range

The RP2040 ADC produces a 12-bit result:

```text
0-4095
```

The firmware converts the raw count to an approximate voltage using:

```c
const float conversion_factor = 3.3f / 4095.0f;
float voltage = raw * conversion_factor;
```

## Initial tests

### Ground

Connecting GPIO26 to ground produced readings near:

```text
0-30 counts
```

### 3.3 V

Connecting GPIO26 to 3V3 produced readings near:

```text
4095 counts
```

### Half-scale divider

Two equal resistors were used as a voltage divider:

```text
3V3 -- R --+-- R -- GND
           |
         GPIO26
```

The expected midpoint voltage is:

```text
3.3 V / 2 = 1.65 V
```

Observed readings were around:

```text
2040-2090 counts
```

with values close to:

```text
2050 counts
1.651 V
```

## Wiring mistake

The first divider attempt was wired incorrectly.

Instead of staying near half-scale, the ADC value gradually decayed toward zero.

After rewiring GPIO26 to the actual junction between the two resistors, the reading stabilized near 1.65 V.

That made the difference between a defined analog node and a floating or poorly connected node very obvious.

## Time-series capture

The firmware was changed to output:

```text
time_ms,raw_adc,voltage
```

with:

```c
sleep_ms(50);
```

giving a target sample rate of 20 Hz.

The first saved dataset contained:

```text
249 samples
12.429 s duration
50.117 ms average sample interval
19.95 Hz average sample rate
```

Measured ADC statistics:

```text
mean:        2064.61 counts
std dev:       19.16 counts
minimum:     2027 counts
maximum:     2095 counts
```

Measured voltage statistics:

```text
mean:        1.6638 V
std dev:     0.0155 V
minimum:     1.633 V
maximum:     1.688 V
```

The next step would be to compare the raw signal with a simple moving-average filter.
