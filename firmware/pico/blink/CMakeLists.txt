cmake_minimum_required(VERSION 3.13)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(fabianpm_blink C CXX ASM)

pico_sdk_init()

add_executable(fabianpm_blink
    main.c
)

target_link_libraries(fabianpm_blink
    pico_stdlib
    pico_cyw43_arch_none
)

pico_add_extra_outputs(fabianpm_blink)
