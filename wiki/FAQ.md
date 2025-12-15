# Frequently Asked Questions

## General Questions

### What is Zelta?
Zelta is an IoT device management platform consisting of:
- **Open-source embedded SDK** (this repository) for device firmware
- **Closed-source cloud platform** for device management, monitoring, and OTA updates
- **Web dashboard** for fleet management and analytics

### Is Zelta free?
- **Embedded SDK**: Yes, completely free and open-source (MIT License)
- **Cloud Platform**: Free tier available, paid plans for production deployments
- See https://zeltasoft.com/pricing for details

### What's the difference between Zelta and AWS IoT / Azure IoT?
- **Zelta**: Purpose-built for device management with built-in OTA, telemetry, and fleet management
- **AWS/Azure IoT**: General-purpose IoT platforms requiring more custom integration
- **Zelta advantage**: Faster time-to-market, lower complexity, better developer experience

## Technical Questions

### Which hardware platforms are supported?
Officially supported:
- ESP32 series (ESP32, ESP32-S3, ESP32-C3)
- Nordic nRF52/nRF53 series
- STM32 series

Community supported:
- Any Zephyr RTOS compatible board

See [Hardware Requirements](Hardware-Requirements) for details.

### What is the minimum RAM/Flash requirement?
- **Minimum**: 64 KB RAM, 256 KB Flash (basic telemetry only)
- **Recommended**: 128 KB RAM, 512 KB Flash (with OTA support)
- **Production**: 256 KB RAM, 1 MB Flash (full features)

### Can I use this without the Zelta cloud platform?
The SDK is designed to work with Zelta's cloud platform. For self-hosted alternatives:
- MQTT broker: You can point to your own broker
- Cloud API: Would require implementing compatible endpoints
- Not officially supported, but technically possible

### Does it work with FreeRTOS / Arduino?
- **Zephyr RTOS**: ✅ Primary and officially supported
- **FreeRTOS**: ⚠️ Possible with porting effort (not officially supported)
- **Arduino**: ❌ Not compatible (different architecture)

### How secure is it?
- TLS 1.2/1.3 encryption for all communication
- Certificate-based device authentication
- Secure credential storage in NVS
- OTA updates with signature verification
- See [TLS Security](TLS-Security) for details

## Development Questions

### How do I get started?
Follow the [Quick Start Guide](Quick-Start) for a 15-minute walkthrough.

### Can I debug my device firmware?
Yes! Supported debugging methods:
- **JTAG/SWD** with OpenOCD, J-Link, or CMSIS-DAP
- **Serial console** via `west attach`
- **Remote logging** to Zelta cloud platform
- **GDB** integration in VS Code

### How do I add custom telemetry?
```c
#include <zelta/telemetry.h>

// Send custom metrics
zelta_telemetry_report("my_sensor", value);
```

See [Telemetry API](API-Telemetry) for advanced usage.

### Can I use custom sensors?
Yes! The SDK has a flexible sensor interface:
- I2C, SPI, UART, ADC supported
- Use Zephyr's sensor subsystem
- Or implement custom drivers

See [Example Sensor Hub](Example-Sensor-Hub).

## OTA Update Questions

### How do OTA updates work?
1. New firmware uploaded to Zelta platform
2. Platform notifies devices of available update
3. Device downloads firmware chunks over MQTT
4. Firmware verified and installed
5. Device reboots into new firmware
6. Rollback on failure

See [OTA Updates](OTA-Updates) for details.

### What if an OTA update fails?
- Automatic rollback to previous firmware
- Update marked as failed in platform
- Device continues running on stable version

### Can I schedule OTA updates?
Yes, through the Zelta dashboard:
- Immediate deployment
- Scheduled rollout
- Staged deployment (percentage-based)
- Canary releases (test on subset first)

### How much bandwidth do OTA updates use?
- Firmware size: Typically 200 KB - 1 MB
- Transfer method: Chunked over MQTT (configurable chunk size)
- Retry logic: Only failed chunks re-downloaded
- Compression: Optional (reduces size ~40%)

## Connectivity Questions

### Which protocols are supported?
- **MQTT**: Primary protocol (recommended)
- **HTTPS**: Alternative for direct REST API calls
- **CoAP**: Planned (not yet implemented)

See [Transport Protocols](Transport-MQTT) for details.

### Can devices work offline?
Yes, with limitations:
- Telemetry queued locally during offline period
- Uploaded when connection restored
- Queue size: Configurable (typically 10-100 messages)
- OTA updates: Require connectivity

### What happens if WiFi disconnects?
- Automatic reconnection with exponential backoff
- Queued messages sent after reconnection
- Configurable retry parameters

### Can I use cellular instead of WiFi?
Yes! Supported cellular modules:
- Nordic nRF9160 (LTE-M/NB-IoT)
- u-blox SARA-R4/R5
- Quectel BG96, BC66
- SIMCom SIM7000

Requires cellular-capable hardware.

## Pricing & Licensing

### Is the SDK really free?
Yes, the embedded SDK is 100% free and open-source under MIT License.

### What about the cloud platform?
- **Free tier**: 10 devices, 1M messages/month
- **Pro**: Starts at $49/month for 100 devices
- **Enterprise**: Custom pricing for large fleets

See https://zeltasoft.com/pricing for current rates.

### Can I use this commercially?
Yes! MIT License allows commercial use without restrictions.

### Do I need to publish my firmware source code?
No, the MIT License does not require you to open-source your application code.

## Troubleshooting

### Device won't connect to MQTT broker
1. Check WiFi credentials in `prj.conf`
2. Verify MQTT broker address and port
3. Confirm API key is correct
4. Enable debug logging: `CONFIG_ZELTA_LOG_LEVEL_DBG=y`
5. Check firewall rules (port 8883 outbound)

### Build errors
1. Update Zephyr SDK: `west update`
2. Clean build: `west build -t pristine`
3. Check board configuration
4. Review [Troubleshooting Build](Troubleshooting-Build)

### Telemetry not appearing in dashboard
1. Verify device shows "online" in dashboard
2. Check MQTT topic format
3. Validate JSON message format
4. Review device logs for errors

### High power consumption
1. Enable sleep mode: `CONFIG_PM=y`
2. Reduce telemetry frequency
3. Increase MQTT keep-alive interval
4. See [Power Management](Power-Management)

## Contributing

### How can I contribute?
We welcome contributions! See [Contributing Guide](Contributing).

Areas needing help:
- Hardware platform support
- Example applications
- Documentation improvements
- Bug reports and fixes

### Where do I report bugs?
- GitHub Issues: https://github.com/afmecofe/zelta/issues
- Security issues: security@zeltasoft.com

### Can I request features?
Yes! Use GitHub Discussions for feature requests:
https://github.com/afmecofe/zelta/discussions

## Support

### Where can I get help?
- **Documentation**: This wiki
- **GitHub Discussions**: Community support
- **Email**: support@zeltasoft.com (commercial customers)
- **Discord**: Coming soon!

### Is commercial support available?
Yes, for production deployments:
- Dedicated support engineer
- SLA guarantees
- Custom feature development
- Contact: sales@zeltasoft.com

## Still have questions?

Ask in [GitHub Discussions](https://github.com/afmecofe/zelta/discussions) or email support@zeltasoft.com.
