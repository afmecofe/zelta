# Quick Start Guide

Get your first Zelta-powered device up and running in 15 minutes.

## Prerequisites

- **Hardware**: ESP32 DevKitC, nRF52840 DK, or supported board
- **Software**: Zephyr SDK 0.16+, West, Python 3.8+
- **Account**: Zelta platform account ([sign up](https://zeltasoft.com))

## Step 1: Install Zephyr SDK

```bash
# Install dependencies (Ubuntu/Debian)
sudo apt update
sudo apt install -y git cmake ninja-build gperf \
  ccache dfu-util device-tree-compiler wget \
  python3-dev python3-pip python3-setuptools python3-tk python3-wheel \
  xz-utils file make gcc gcc-multilib g++-multilib libsdl2-dev

# Install West
pip3 install --user -U west

# Initialize workspace
west init ~/zephyrproject
cd ~/zephyrproject
west update
west zephyr-export
pip3 install --user -r ~/zephyrproject/zephyr/scripts/requirements.txt
```

## Step 2: Clone Zelta SDK

```bash
cd ~/zephyrproject
git clone --recursive https://github.com/didavie/Zelta.git
cd Zelta/embedded
```

## Step 3: Configure Your Device

Create a Zelta account and get your device credentials:

1. Sign up at https://zeltasoft.com
2. Create an organization
3. Add a new device and copy the credentials

Edit `samples/basic_telemetry/prj.conf`:

```ini
# Device credentials (from Zelta dashboard)
CONFIG_ZELTA_PRODUCT_ID="your-product-uuid"
CONFIG_ZELTA_DEVICE_ID="your-device-uuid"
CONFIG_ZELTA_API_KEY="your-device-api-key"

# MQTT broker
CONFIG_ZELTA_MQTT_BROKER="mqtt.zeltasoft.com"
CONFIG_ZELTA_MQTT_PORT=8883
CONFIG_ZELTA_TLS_ENABLED=y

# Features
CONFIG_ZELTA_TELEMETRY=y
CONFIG_ZELTA_OTA_UPDATES=y
```

## Step 4: Build Firmware

For ESP32:
```bash
west build -b esp32_devkitc_wrover samples/basic_telemetry
```

For nRF52840:
```bash
west build -b nrf52840dk_nrf52840 samples/basic_telemetry
```

## Step 5: Flash Your Device

```bash
west flash
```

## Step 6: Monitor Output

```bash
west attach
```

You should see:
```
*** Booting Zephyr OS build v3.5.0 ***
[00:00:00.123] <inf> zelta: Initializing Zelta SDK v1.0.0
[00:00:00.456] <inf> zelta: Provisioning device...
[00:00:01.234] <inf> zelta: Connected to mqtt.zeltasoft.com:8883
[00:00:01.567] <inf> zelta: Device online and ready
[00:00:02.000] <inf> telemetry: Sent temperature: 25.3°C
```

## Step 7: View Data in Dashboard

1. Log in to https://app.zeltasoft.com
2. Navigate to your device
3. See real-time telemetry data streaming in

## Next Steps

- [Send Custom Telemetry](Telemetry-Reporting)
- [Handle Remote Commands](Command-Handling)
- [Enable OTA Updates](OTA-Updates)
- [Optimize for Low Power](Power-Management)

## Troubleshooting

**Build fails with "cannot find zelta/device.h"**
- Run `west update` to refresh dependencies
- Ensure you're in the embedded directory

**Device won't connect**
- Check WiFi credentials in `prj.conf`
- Verify API key is correct
- Enable debug logging: `CONFIG_ZELTA_LOG_LEVEL_DBG=y`

**No telemetry in dashboard**
- Confirm device shows as "online" in dashboard
- Check MQTT topics match (see [MQTT Topics](MQTT-Topics))
- Review device logs for transmission errors
