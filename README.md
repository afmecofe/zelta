# Zelta Embedded SDK

Open-source embedded firmware SDK for the Zelta IoT device management platform. This SDK enables IoT devices to securely connect, communicate, and receive over-the-air updates from the Zelta cloud platform.

> **Note:** This is the open-source component of Zelta. The cloud platform, web dashboard, and management SDK are closed-source commercial products.

## Overview

Zelta Embedded SDK provides production-ready firmware for IoT devices built on **Zephyr RTOS**. It handles device provisioning, secure MQTT communication, telemetry reporting, and OTA firmware updates, allowing you to focus on your application logic.

### Key Features

- 🔐 **Secure Device Provisioning** - Automated device registration with the Zelta platform
- 📡 **MQTT Connectivity** - Bidirectional communication with TLS encryption
- 📊 **Telemetry & Logging** - Real-time device metrics and event streaming
- 🔄 **OTA Updates** - Remote firmware updates with rollback support
- ⚡ **Low Power Mode** - Optimized for battery-powered devices
- 🛡️ **Security First** - End-to-end encryption, certificate-based authentication
- 📱 **Multi-Platform** - ESP32, nRF52, STM32, and more

## Architecture

The SDK integrates with the Zelta cloud platform components:

```
┌─────────────────────┐
│  Your Application   │
├─────────────────────┤
│  Zelta Embedded SDK │ ◄── This Repository (Open Source)
└──────────┬──────────┘
           │ MQTT/TLS
           ▼
┌─────────────────────┐
│  Zelta MQTT Bridge  │
├─────────────────────┤
│  Zelta Cloud API    │ ◄── Closed Source
├─────────────────────┤
│  Zelta Web Dashboard│
└─────────────────────┘
```

## Hardware Support

Tested and verified on:

- **ESP32** (ESP32-DevKitC, ESP32-WROVER)
- **Nordic nRF52** (nRF52840 DK, nRF52833)
- **STM32** (STM32F4, STM32L4 series)
- **Custom boards** via Zephyr device tree

## Technology Stack

- **RTOS**: [Zephyr RTOS](https://www.zephyrproject.org/) 3.x
- **Build System**: CMake + West
- **Protocol**: MQTT 3.1.1/5.0 with TLS 1.2/1.3
- **Security**: mbedTLS, Hardware crypto acceleration
- **Storage**: NVS (Non-Volatile Storage) for credentials and config

## Quick Start

### Prerequisites

- [Zephyr SDK](https://docs.zephyrproject.org/latest/develop/getting_started/index.html) installed
- West build tool
- Python 3.8+
- A Zelta platform account (contact sales@zeltasoft.com)

### Building Firmware

```bash
# Clone with parent repository
git clone --recursive https://github.com/didavie/Zelta.git
cd Zelta/embedded

# Build for your target board
west build -b esp32_devkitc_wrover samples/basic_telemetry

# Flash to device
west flash
```

### Configuration

Create a `prj.conf` file in your application:

```ini
# Zelta Configuration
CONFIG_ZELTA_DEVICE_ID="your-device-id"
CONFIG_ZELTA_MQTT_BROKER="mqtt.zeltasoft.com"
CONFIG_ZELTA_MQTT_PORT=8883
CONFIG_ZELTA_TLS_ENABLED=y

# Enable features
CONFIG_ZELTA_TELEMETRY=y
CONFIG_ZELTA_OTA_UPDATES=y
CONFIG_ZELTA_LOGGING=y
```

### Basic Usage

```c
#include <zelta/device.h>
#include <zelta/telemetry.h>

void main(void) {
    // Initialize Zelta SDK
    zelta_init();
    
    // Provision device (first boot only)
    zelta_provision();
    
    // Connect to platform
    zelta_connect();
    
    while (1) {
        // Send telemetry
        zelta_telemetry_report("temperature", sensor_read_temp());
        zelta_telemetry_report("battery", battery_level());
        
        // Check for commands/updates
        zelta_process_messages();
        
        k_sleep(K_SECONDS(60));
    }
}
```

## Samples

Explore ready-to-run examples:

- **basic_telemetry** - Simple sensor data reporting
- **provisioning** - Device registration flow
- **ota_update** - Firmware update with rollback
- **low_power** - Battery-optimized operation
- **sensor_hub** - Multi-sensor data aggregation

## Development

### Project Structure

```
embedded/
├── CMakeLists.txt          # Root build configuration
├── Kconfig                 # Configuration options
├── include/
│   └── zelta/              # Public SDK headers
├── src/
│   ├── device.c            # Device management
│   ├── mqtt.c              # MQTT client
│   ├── telemetry.c         # Telemetry reporting
│   ├── ota.c               # OTA update handler
│   └── provisioning.c      # Device provisioning
├── samples/                # Example applications
└── tests/                  # Unit and integration tests
```

### Building for Custom Hardware

1. Create a custom board definition in `zephyr/boards/`
2. Configure device tree for your peripherals
3. Set hardware-specific Kconfig options
4. Build with `-b your_custom_board`

### Testing

```bash
# Run unit tests
west build -t run tests/unit

# Run on hardware (requires device connected)
west build -t flash tests/integration
west attach
```

## Integration with Zelta Platform

This SDK works exclusively with the Zelta cloud platform:

1. **Sign up** for a Zelta account at https://zeltasoft.com
2. **Create an organization** and project in the web dashboard
3. **Generate device credentials** for your fleet
4. **Configure** the SDK with your organization ID and API endpoint
5. **Deploy** firmware to your devices

The platform provides:
- Real-time device monitoring and control
- Fleet-wide OTA updates with staged rollouts
- Usage analytics and reporting
- RBAC and multi-tenancy
- REST API and management SDK

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution

- Additional hardware platform support
- Protocol optimizations
- Power consumption improvements
- Example applications
- Documentation and tutorials

## Security

Report security vulnerabilities to security@zeltasoft.com. See [SECURITY.md](../SECURITY_ANALYSIS.md) for our security policy.

## License

This embedded SDK is open-source software licensed under the [MIT License](LICENSE).

The Zelta cloud platform, web dashboard, and management SDK are proprietary software. Contact sales@zeltasoft.com for licensing information.

## Support

- **Documentation**: https://docs.zeltasoft.com
- **Issues**: https://github.com/afmecofe/zelta/issues
- **Discussions**: https://github.com/afmecofe/zelta/discussions
- **Commercial Support**: support@zeltasoft.com

## Roadmap

- [ ] LoRaWAN support
- [ ] BLE mesh networking
- [ ] Edge AI/ML inference
- [ ] Thread/Matter protocol support
- [ ] Enhanced power profiling tools

---

Built with ❤️ for the IoT community by the Zelta team.
