cmake_minimum_required(VERSION 3.13)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(fabianpm_hello_usb C CXX ASM)

pico_sdk_init()

add_executable(fabianpm_hello_usb
    main.c
)

target_link_libraries(fabianpm_hello_usb
    pico_stdlib
)

pico_enable_stdio_usb(fabianpm_hello_usb 1)
pico_enable_stdio_uart(fabianpm_hello_usb 0)

pico_add_extra_outputs(fabianpm_hello_usb)