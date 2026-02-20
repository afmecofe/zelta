# Platform Support

Zelta is **platform-agnostic** and works with any system that supports MQTT or HTTPS communication.

## Platform Categories

### ✅ Fully Supported (Reference Implementation Available)

These platforms have ready-to-use code in the repository:

#### Zephyr RTOS
- **Implementation**: Complete C library with CMake integration
- **Platforms**: ESP32, nRF52, nRF53, STM32, QEMU, and 300+ boards
- **Features**: Full SDK, OTA, telemetry, commands, low power
- **Docs**: [Zephyr Integration Guide](Zephyr-Integration)

#### Embedded Linux
- **Implementation**: C daemon with systemd service
- **Distributions**: Yocto, Buildroot, Debian, Ubuntu, OpenWrt
- **Features**: Full SDK, OTA, telemetry, logging
- **Docs**: [Linux Integration Guide](Linux-Integration)

### 🔧 Community Supported (Port Available)

Community members have ported Zelta to these platforms:

#### FreeRTOS
- **Status**: Community port available
- **Platforms**: ESP32 (ESP-IDF), STM32, Renesas
- **Docs**: [FreeRTOS Integration](FreeRTOS-Integration)

#### Arduino/ESP-IDF
- **Status**: Example implementation
- **Platforms**: ESP32, ESP8266
- **Docs**: [Arduino Integration](Arduino-Integration)

### 🌐 Protocol Compatible (Implement Yourself)

Zelta's open protocol can be implemented on any platform:

#### High-Level Languages
- **Python/MicroPython** - Perfect for Raspberry Pi, Linux SBCs
- **Node.js/JavaScript** - IoT gateways, web-connected devices
- **Go** - High-performance edge devices
- **Rust** - Safety-critical embedded systems
- **Java/Kotlin** - Android devices, industrial gateways

#### Embedded Platforms
- **Bare Metal** - Any MCU with networking
- **mbed OS** - ARM Cortex-M devices
- **RT-Thread** - Chinese RTOS
- **NuttX** - POSIX-compliant RTOS
- **Azure RTOS** - ThreadX-based systems

#### Edge/Gateway Devices
- **Raspberry Pi** - Full Linux support
- **BeagleBone** - Linux with systemd
- **NVIDIA Jetson** - AI edge devices
- **Intel NUC** - Industrial gateways

## Platform Requirements

### Minimum Requirements (MQTT)

To run Zelta over MQTT, you need:

- **RAM**: 64 KB (128 KB recommended)
- **Flash**: 256 KB (512 KB for OTA support)
- **Networking**: WiFi, Ethernet, Cellular, or LoRaWAN
- **TLS Support**: TLS 1.2+ library (mbedTLS, OpenSSL, etc.)
- **MQTT Client**: Any MQTT 3.1.1 or 5.0 library

### Minimum Requirements (HTTPS)

To run Zelta over REST API, you need:

- **RAM**: 128 KB (256 KB recommended)
- **Flash**: 512 KB
- **Networking**: Same as MQTT
- **TLS Support**: Same as MQTT
- **HTTP Client**: Any HTTPS client library

### Recommended for Production

- **RAM**: 256 KB+
- **Flash**: 1 MB+ (for dual-bank OTA)
- **Hardware Crypto**: AES, SHA-256 acceleration
- **Watchdog Timer**: For reliability
- **RTC**: For timestamps

## RTOS Compatibility Matrix

| RTOS | Status | Effort | Notes |
|------|--------|--------|-------|
| **Zephyr** | ✅ Native | None | Reference implementation |
| **Linux** | ✅ Native | None | Daemon + systemd service |
| **FreeRTOS** | 🔧 Port | Low | Port mbedTLS + MQTT client |
| **mbed OS** | 🌐 DIY | Low | Use mbed MQTT library |
| **RT-Thread** | 🌐 DIY | Medium | Implement protocol layer |
| **NuttX** | 🌐 DIY | Low | Similar to Linux approach |
| **Azure RTOS** | 🌐 DIY | Medium | Use NetX Duo MQTT |
| **Bare Metal** | 🌐 DIY | High | Implement full stack |

## Language Compatibility

| Language | MQTT Library | Recommended For |
|----------|--------------|-----------------|
| **C** | libmosquitto, paho-mqtt | Zephyr, FreeRTOS, bare metal |
| **C++** | paho-mqttpp, MQTT-C | Arduino, mbed OS |
| **Python** | paho-mqtt | Linux, Raspberry Pi |
| **JavaScript** | mqtt.js | Node.js, gateways |
| **Go** | paho.mqtt.golang | Edge servers |
| **Rust** | rumqtt, paho-mqtt-rust | Safety-critical |
| **Java** | paho-mqtt-java | Android, industrial |

## Hardware Platform Examples

### Microcontrollers

| MCU Family | RTOS | Connection | Notes |
|------------|------|------------|-------|
| **ESP32** | Zephyr, FreeRTOS, Arduino | WiFi | Best for WiFi projects |
| **nRF52** | Zephyr | BLE, Thread | Ultra-low power |
| **nRF9160** | Zephyr | LTE-M, NB-IoT | Cellular built-in |
| **STM32** | Zephyr, FreeRTOS, mbed | WiFi module, Ethernet | Industrial grade |
| **RP2040** | FreeRTOS, Arduino | WiFi (Pico W) | Low cost |
| **CC3220** | FreeRTOS | WiFi | Integrated WiFi |

### Single Board Computers

| SBC | OS | Connection | Notes |
|-----|-----|------------|-------|
| **Raspberry Pi** | Linux (Debian) | WiFi, Ethernet | Full Linux support |
| **BeagleBone** | Linux (Debian, Yocto) | Ethernet, WiFi | Industrial I/O |
| **NVIDIA Jetson** | Linux (Ubuntu) | Ethernet, WiFi | AI edge |
| **Orange Pi** | Linux (Armbian) | Ethernet | Low cost |
| **Rock Pi** | Linux | Ethernet | High performance |

### Cellular Modules

| Module | Interface | Notes |
|--------|-----------|-------|
| **SIMCom SIM7000** | AT commands | LTE Cat-M1, NB-IoT |
| **Quectel BG96** | AT commands | LTE Cat-M1, NB-IoT |
| **u-blox SARA-R4** | AT commands | LTE Cat-M1 |
| **nRF9160** | Native Zephyr | Best integration |

## Choosing Your Platform

### For Prototyping

- **Raspberry Pi Zero W** - Easy Linux development, $10
- **ESP32-DevKitC** - WiFi, low cost, $10
- **nRF52840 DK** - BLE, excellent tools, $50

### For Battery-Powered Devices

- **nRF52840** (Zephyr) - Ultra-low power, 1-5 µA sleep
- **nRF9160** (Zephyr) - Cellular with PSM mode
- **STM32L4** (Zephyr/FreeRTOS) - Low power MCU

### For Industrial Applications

- **STM32F4/H7** - Robust, wide temp range
- **BeagleBone Industrial** - Linux with industrial I/O
- **Toradex** modules - Industrial SoM

### For High-Volume Production

- **ESP32-C3** - Low cost, WiFi, RISC-V
- **nRF52832** - BLE, ultra-low power
- **Custom STM32 board** - Design your own

## Platform Migration

Already have firmware? Here's how to add Zelta:

### From AWS IoT Core
- Replace AWS IoT SDK with Zelta protocol
- Change MQTT topics and message format
- Simpler authentication (API key vs AWS certs)

### From Azure IoT Hub
- Replace Azure IoT SDK with Zelta protocol
- Simpler connection (no device twin needed)
- Standard MQTT instead of Azure-specific

### From Particle.io
- Replace Particle Cloud with Zelta
- More control over protocol and data
- No vendor lock-in

### From Custom MQTT
- Adapt your topics to Zelta format
- Add API key authentication
- Implement OTA update protocol

## Next Steps

- [Choose Your Integration Path](Integration-Paths)
- [Zephyr Integration](Zephyr-Integration) - For RTOS projects
- [Linux Integration](Linux-Integration) - For embedded Linux
- [Custom Integration](Custom-Integration) - For other platforms
