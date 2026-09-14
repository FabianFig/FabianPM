# FabianPM

FabianPM is a DIY bicycle crank power meter built around a Raspberry Pi Pico W.

The goal is to measure crank torque using strain gauges, combine it with crank angular velocity, and eventually broadcast power data to a bike computer over BLE or ANT+.

I am using the project to learn embedded development, instrumentation, signal processing, and the practical hardware involved in measuring very small strain signals.

## Current progress

- Raspberry Pi Pico W C/C++ toolchain running on Arch Linux
- Built and flashed first firmware
- USB serial communication working
- ADC measurements working on GPIO26/ADC0
- Verified ADC response at ground, approximately 1.65 V, and 3.3 V
- Captured the first timestamped 20 Hz ADC dataset
- Started Python analysis of captured data
