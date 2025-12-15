# Zelta Embedded SDK

Open-source embedded firmware SDK for the Zelta IoT device management platform. This SDK is **platform-agnostic** and works with any embedded system that can communicate via MQTT or HTTPS.

> **Note:** This is the open-source component of Zelta. The cloud platform, web dashboard, and management tools are closed-source commercial products.

## Overview

The Zelta Embedded SDK provides a protocol implementation for connecting IoT devices to the Zelta cloud platform. It's **not limited to any specific RTOS** - the protocol is open and can be implemented on any platform.

### Supported Platforms

- ✅ **Zephyr RTOS** - Reference implementation provided
- ✅ **Linux** (Yocto, Buildroot, Debian, etc.) - Full support
- ✅ **FreeRTOS** - Port the reference implementation
- ✅ **Bare Metal** - Implement the protocol directly
- ✅ **Any platform with MQTT or HTTPS** - Protocol is platform-agnostic

### Key Features

- 🔐 **Secure Device Provisioning** - Register devices with the platform
- 📡 **MQTT or HTTPS Communication** - Choose your transport protocol
- 📊 **Telemetry Reporting** - Engine, fluids, battery, location, sensors, diagnostics
- 🔄 **OTA Updates** - Remote firmware updates with rollback support
- ⚡ **Low Power Support** - Optimized for battery-powered devices
- 🛡️ **Security** - TLS encryption, API key or certificate authentication
- 📱 **Multi-Platform** - Works on any hardware that supports networking

## Architecture

Zelta uses a **protocol-first approach**. Any device that can speak MQTT or HTTPS can integrate with the platform:

```
┌─────────────────────────────────────────┐
│     Your Device Application             │
│  (Any OS: Zephyr, Linux, FreeRTOS, etc.)│
├─────────────────────────────────────────┤
│    Zelta Protocol Implementation        │ ◄── Open Protocol (MQTT + REST)
│  (Reference: C for Zephyr, portable)    │
└──────────────┬──────────────────────────┘
               │ MQTT/TLS or HTTPS
               ▼
┌─────────────────────────────────────────┐
│        MQTT Bridge (Mosquitto)          │
│  Converts MQTT ↔ Supabase Functions     │
├─────────────────────────────────────────┤
│      Zelta Cloud Platform (SaaS)        │ ◄── Closed Source
│  - Device Management                    │
│  - OTA Update Orchestration             │
│  - Telemetry Processing                 │
│  - Web Dashboard                        │
└─────────────────────────────────────────┘
```

### Protocol Overview

The Zelta protocol is **simple and open**:

1. **Device Authentication**: API key or TLS client certificates
2. **Communication**: MQTT topics or HTTPS REST endpoints
3. **Telemetry**: JSON payloads sent to specific topics/endpoints
4. **OTA Updates**: Poll for updates, download chunks, verify, install
5. **Commands**: Subscribe to command topics for remote control

You can implement this protocol in **any language** on **any platform**.

## Implementation Options

### Option 1: Reference C Library (Zephyr RTOS)

Pre-built integration for Zephyr RTOS with full features:

```c
#include <zelta/device.h>
#include <zelta/telemetry.h>

void main(void) {
    zelta_init();
    zelta_connect();
    
    while (1) {
        zelta_telemetry_report("temperature", 25.3);
        zelta_process_messages();
        k_sleep(K_SECONDS(60));
    }
}
```

### Option 2: Linux Integration (Yocto/Buildroot/Debian)

Run as a systemd service on embedded Linux:

```bash
# Install dependencies
apt-get install mosquitto-clients libmosquitto-dev libcurl4-openssl-dev

# Build the agent
git clone https://github.com/afmecofe/zelta.git
cd zelta
mkdir build && cd build
cmake .. && make

# Run as daemon
systemd enable zelta-agent
systemd start zelta-agent
```

### Option 3: Custom Implementation (Any Platform)

Implement the protocol directly using our API documentation:

```python
# Python example
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.username_pw_set("device-id", "api-key")
client.connect("mqtt.zeltasoft.com", 8883)

# Send telemetry
topic = f"zelta/{product_id}/{device_id}/up/telemetry/sensors"
payload = json.dumps({"temperature": 25.3, "humidity": 60.0})
client.publish(topic, payload, qos=1)
```

Works with: Python, Node.js, Go, Rust, Java, C#, Arduino, MicroPython, etc.

## Quick Start

### For Zephyr RTOS Users

```bash
# Clone with parent repository
git clone --recursive https://github.com/didavie/Zelta.git
cd Zelta/embedded

# Build for your target board
west build -b esp32_devkitc_wrover samples/basic_telemetry
west flash
```

### For Linux/Yocto Users

```bash
# Add to your Yocto layer
bitbake zelta-agent

# Or build manually
git clone https://github.com/afmecofe/zelta.git
cd zelta && mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make && sudo make install
```

### For Other Platforms

1. Read the [Protocol Documentation](https://github.com/afmecofe/zelta/wiki/Protocol-Reference)
2. Implement MQTT client or HTTPS client
3. Follow the [Integration Guide](https://github.com/afmecofe/zelta/wiki/Custom-Integration)

## Protocol Documentation

The Zelta protocol is **open and documented**. You don't need our SDK if you prefer to implement it yourself.

### MQTT Topics

```
Device → Cloud:
  zelta/{product_id}/{device_id}/up/status          - Status updates
  zelta/{product_id}/{device_id}/up/heartbeat       - Keep-alive (every 60s)
  zelta/{product_id}/{device_id}/up/check           - Check for firmware updates
  zelta/{product_id}/{device_id}/up/telemetry/*     - Telemetry data

Cloud → Device:
  zelta/{product_id}/{device_id}/down/command       - Remote commands
  zelta/{product_id}/{device_id}/down/response      - Command responses
  zelta/{product_id}/{device_id}/down/firmware      - Firmware chunks
```

### REST API Endpoints

```
POST https://api.zeltasoft.com/check-update
  Body: {"device_id": "...", "current_version": "1.0.0"}
  
POST https://api.zeltasoft.com/report-telemetry
  Body: {"device_id": "...", "type": "sensors", "data": {...}}

POST https://api.zeltasoft.com/report-status
  Body: {"device_id": "...", "status": "online", "version": "1.0.0"}
```

See [API Documentation](https://github.com/afmecofe/zelta/wiki/API-Reference) for complete details.

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
