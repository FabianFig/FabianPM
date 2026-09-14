cmake_minimum_required(VERSION 3.13)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(fabianpm_adc_read C CXX ASM)

pico_sdk_init()

add_executable(fabianpm_adc_read
    main.c
)

target_link_libraries(fabianpm_adc_read
    pico_stdlib
    hardware_adc
)

pico_enable_stdio_usb(fabianpm_adc_read 1)
pico_enable_stdio_uart(fabianpm_adc_read 0)

pico_add_extra_outputs(fabianpm_adc_read)
