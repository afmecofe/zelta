# Hardware Requirements

Minimum and recommended hardware specifications for running Zelta Embedded SDK.

## Minimum Requirements

### MCU Specifications
- **Architecture**: ARM Cortex-M3 or higher, RISC-V RV32IMAC, Xtensa LX6/LX7
- **Flash**: 256 KB (512 KB recommended for OTA)
- **RAM**: 64 KB (128 KB recommended)
- **Clock Speed**: 48 MHz minimum

### Connectivity
- **WiFi**, **Ethernet**, **Cellular** (LTE-M, NB-IoT, 2G/3G/4G), or **LoRaWAN**
- TLS 1.2+ support (hardware crypto accelerator recommended)

### Storage
- **Non-Volatile Storage (NVS)**: 8 KB minimum for credentials and config
- **OTA Updates**: 2x firmware size for dual-bank flash

## Recommended Specifications

### For Full Features
- **Flash**: 1 MB+ (enables all SDK features + application code)
- **RAM**: 256 KB+ (comfortable for complex applications)
- **Hardware Crypto**: AES, SHA-256 acceleration
- **RTC**: Real-time clock for timestamps
- **Watchdog**: Hardware watchdog timer

### Optional Peripherals
- **GPS/GNSS**: For location tracking
- **Sensors**: I2C, SPI, ADC interfaces
- **External Flash**: For data logging, extended OTA storage
- **Battery Management**: ADC for battery monitoring

## Tested Platforms

### ✅ ESP32 Series (Espressif)

| Board | Flash | RAM | Crypto | Notes |
|-------|-------|-----|--------|-------|
| **ESP32-DevKitC** | 4 MB | 520 KB | ✅ | Best for WiFi projects |
| **ESP32-WROVER** | 4-16 MB | 8 MB PSRAM | ✅ | Large applications |
| **ESP32-S3** | 8 MB | 512 KB | ✅ | Latest, best performance |
| **ESP32-C3** | 4 MB | 400 KB | ✅ | Low-cost RISC-V |

**Pros**: Excellent WiFi, affordable, large community  
**Cons**: Higher power consumption

### ✅ Nordic nRF52/nRF53 Series

| Board | Flash | RAM | Crypto | Notes |
|-------|-------|-----|--------|-------|
| **nRF52840 DK** | 1 MB | 256 KB | ✅ | BLE, USB, NFC |
| **nRF52833** | 512 KB | 128 KB | ✅ | Cost-optimized |
| **nRF5340 DK** | 1 MB | 512 KB | ✅ | Dual-core, BLE 5.3 |
| **nRF9160** | 1 MB | 256 KB | ✅ | **Cellular LTE-M/NB-IoT** |

**Pros**: Ultra-low power, excellent for battery devices  
**Cons**: WiFi requires external module (except nRF7002)

### ✅ STM32 Series (ST Microelectronics)

| Series | Flash | RAM | Crypto | Notes |
|--------|-------|-----|--------|-------|
| **STM32F4** | 512 KB - 2 MB | 128-384 KB | ✅ | Popular, Cortex-M4 |
| **STM32L4** | 256 KB - 1 MB | 64-320 KB | ✅ | Ultra-low power |
| **STM32H7** | 1-2 MB | 512 KB - 1 MB | ✅ | High performance |
| **STM32WL** | 256 KB | 64 KB | ✅ | **Integrated LoRa** |

**Pros**: Wide variety, excellent peripherals  
**Cons**: Requires external WiFi/cellular module

### ⚠️ Borderline Support

| MCU | Flash | RAM | Status | Notes |
|-----|-------|-----|--------|-------|
| **nRF52832** | 512 KB | 64 KB | Limited | OTA difficult, tight memory |
| **ESP8266** | 1 MB | 80 KB | Not recommended | RAM too constrained |
| **STM32F1** | 64-512 KB | 20-64 KB | Not recommended | Old architecture |

## Feature-Specific Requirements

### Basic Telemetry Only
- Flash: 256 KB
- RAM: 64 KB
- Example: Periodic sensor readings, no OTA

### Telemetry + OTA Updates
- Flash: 512 KB (dual-bank) or 1 MB
- RAM: 128 KB
- Requires: Dual-bank flash or external storage

### Full SDK (Telemetry + OTA + Commands + Logging)
- Flash: 512 KB - 1 MB
- RAM: 256 KB
- Recommended for production deployments

### Edge Computing (Local Processing)
- Flash: 1 MB+
- RAM: 512 KB+
- For: ML inference, data aggregation

## Power Consumption

### Active (Transmitting)
- **WiFi**: 150-300 mA
- **Cellular LTE-M**: 100-200 mA
- **BLE**: 10-20 mA

### Idle (Connected)
- **WiFi**: 15-30 mA
- **Cellular PSM**: 1-5 mA
- **BLE**: 0.5-2 mA

### Deep Sleep
- **ESP32**: 10-150 µA
- **nRF52**: 1-5 µA
- **STM32L4**: 0.5-2 µA

See [Power Management](Power-Management) for optimization strategies.

## Connectivity Options

### WiFi (Most Common)
- **Best for**: Fixed installation, continuous power
- **Range**: 50-100m indoors
- **Data rate**: High (1-100 Mbps)
- **Power**: Moderate-High

### Cellular (LTE-M / NB-IoT)
- **Best for**: Mobile devices, wide area coverage
- **Range**: Kilometers
- **Data rate**: Low-Moderate (100 kbps - 1 Mbps)
- **Power**: Low (with PSM)
- **Cost**: Requires SIM card, data plan

### Bluetooth LE
- **Best for**: Short-range, low-power sensors
- **Range**: 10-100m
- **Data rate**: Low (125 kbps - 2 Mbps)
- **Power**: Very low
- **Limitation**: Requires BLE gateway

### LoRaWAN
- **Best for**: Long-range, low-data rate sensors
- **Range**: 2-15 km
- **Data rate**: Very low (0.3-50 kbps)
- **Power**: Very low
- **Limitation**: Requires LoRaWAN gateway

## Storage Requirements

### Credentials & Configuration
- Device ID, API keys: ~256 bytes
- TLS certificates: 1-4 KB
- Configuration: 1-2 KB
- **Total**: ~8 KB NVS

### Firmware
- SDK base: 150-300 KB
- Application code: 50-500 KB
- **Total**: 200 KB - 1 MB

### OTA Updates
- Current firmware: 200 KB - 1 MB
- Update firmware: 200 KB - 1 MB (dual-bank)
- Scratch space: 8-16 KB
- **Total**: 400 KB - 2 MB flash

### Data Logging (Optional)
- Logs: 10-100 KB
- Offline telemetry buffer: 10-50 KB
- **External flash recommended**

## Recommended Development Kits

### For Beginners
- **ESP32-DevKitC**: ~$10, great for learning
- **nRF52840 DK**: ~$50, excellent tools

### For Production
- **ESP32-S3**: Best WiFi performance
- **nRF9160 DK**: Best for cellular
- **Custom board**: Use reference designs

## Custom Hardware Design

When designing your own board:

1. **Use proven reference designs** (ESP32-WROVER, nRF52840 DK schematics)
2. **Include JTAG/SWD debug header** for development
3. **Add test points** for power rails, key signals
4. **Include hardware watchdog** for reliability
5. **Design for OTA** with dual-bank flash or external storage
6. **Add antenna tuning components** for wireless
7. **Include power measurement** circuitry for optimization

See [Custom Boards](Custom-Boards) for detailed design guidelines.

## See Also

- [Quick Start](Quick-Start)
- [Power Management](Power-Management)
- [OTA Updates](OTA-Updates)
