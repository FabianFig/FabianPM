# Decision 001 - Firmware Platform

## Status

Accepted

## Context

FabianPM will need a microcontroller platform that can handle:

- ADC and sensor acquisition
- timing and signal-processing work
- USB communication during development
- BLE support for eventual cycling-power broadcasting
- low-level embedded C/C++ development

The project is also intended to be a learning project, so direct access to peripherals and the embedded toolchain is useful.

## Decision

Use the Raspberry Pi Pico W with the Raspberry Pi Pico C/C++ SDK.

Build firmware with CMake and Ninja using the ARM GNU embedded toolchain.

Current toolchain:

```text
Raspberry Pi Pico W
RP2040
Pico C/C++ SDK
CMake
Ninja
arm-none-eabi-gcc
```

Reasons
Raspberry Pi Pico W
The Pico W provides:

- RP2040 microcontroller
- onboard ADC inputs
- USB device support
- Wi-Fi and Bluetooth hardware through the CYW43
- low cost
- straightforward breadboard prototyping
  The wireless capability is relevant to the long-term goal of broadcasting cycling-power data.
  C/C++ SDK
  The native Pico SDK was chosen instead of beginning with MicroPython.
  The project will eventually need direct control over:
- ADC sampling
- timers
- interrupts
- communication peripherals
- wireless services
- timing-sensitive acquisition
  Using C/C++ from the beginning also keeps the firmware closer to the type of embedded implementation expected for a finished device.

### CMake and Ninja

CMake is the build system used by the Pico SDK and manages source files, SDK libraries, board configuration, and generated outputs.
Ninja is used as the build backend because it provides a simple and fast incremental build process.
Consequences
The project requires more initial setup than a MicroPython-based workflow.
In return, the firmware has direct access to the RP2040 hardware and Pico SDK APIs, and the development environment can scale into more advanced acquisition and wireless work later in the project.

#### Current result

The toolchain has successfully built and flashed:

- onboard LED blink firmware
- USB CDC serial firmware
- ADC acquisition firmware
  The current firmware can sample GPIO26 / ADC0, convert readings to voltage, timestamp measurements, and stream data over USB serial.
