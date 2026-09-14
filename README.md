# FabianPM

FabianPM is a DIY bicycle crank power meter built around a Raspberry Pi Pico W.

The goal is to measure crank torque using strain gauges, combine it with crank angular velocity, and eventually broadcast power data to a bike computer over BLE or ANT+.

I am using the project to learn embedded development, instrumentation, signal processing, and the practical hardware involved in measuring very small strain signals.
I compared the raw signal against 5-sample, 10-sample, and 20-sample moving averages.
The measured standard deviation decreased to:

````text
5-sample:   0.0065 V
10-sample:  0.0038 V
20-sample:  0.0023 V

### ADC filtering experiment

The first ADC capture used a fixed resistor-divider input at approximately 1.65 V and a target sampling rate of 20 Hz.

The measured capture contained:

```text
249 samples
12.429 s duration
19.95 Hz average sample rate
1.6638 V mean voltage
0.0155 V raw standard deviation

## Current progress

- Raspberry Pi Pico W C/C++ toolchain running on Arch Linux
- Built and flashed first firmware
- USB serial communication working
- ADC measurements working on GPIO26/ADC0
- Verified ADC response at ground, approximately 1.65 V, and 3.3 V
- Captured the first timestamped 20 Hz ADC dataset
- Started Python analysis of captured data
````
