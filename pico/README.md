# Zelta Embedded SDK

Open-source firmware components for connecting devices to the [Zelta](https://zeltasoft.com) IoT platform.

> The cloud platform, web dashboard, and management tools are closed-source commercial products.

---

## Contents

| Path | Description |
|---|---|
| `pico/modbus_rtu_slave.py` | MicroPython Modbus RTU slave for Raspberry Pi Pico |

---

## `pico/modbus_rtu_slave.py`

A zero-dependency Modbus RTU slave implementation in MicroPython for the **Raspberry Pi Pico** (RP2040). Communicates over USB CDC, bypassing the REPL so raw Modbus bytes flow cleanly.

### Supported Function Codes

| FC | Name | Direction |
|---|---|---|
| FC01 | Read Coils | Read |
| FC03 | Read Holding Registers | Read |
| FC05 | Write Single Coil | Write |
| FC06 | Write Single Register | Write |
| FC15 (0x0F) | Write Multiple Coils | Write |
| FC16 (0x10) | Write Multiple Registers | Write |

Writes update in-memory tables; a subsequent read reflects the change.

### Flash

```bash
mpremote connect /dev/ttyACM0 cp pico/modbus_rtu_slave.py :main.py + reset
```

### Default Configuration

```python
DEVICE_ADDR  = 1
HOLDING_REGS = [100 + i * 10 for i in range(64)]   # 64 r/w registers
COILS        = [i % 2         for i in range(64)]   # 64 r/w coils
```

Change `DEVICE_ADDR` at the top of the file to match your Modbus network.

### VS Code Extension Settings (Serial Monitor / Modbus extension)

```
Baud:       9600
Unit ID:    1
Start:      0
Count:      10
```

### Notes

- `micropython.kbd_intr(-1)` disables Ctrl+C so `0x03` is not treated as a keyboard interrupt.
- `uos.dupterm(None, 1)` detaches the REPL from USB CDC so `0x01` (Ctrl+A) does not switch to raw REPL mode.
- Compatible with any MicroPython build that includes `uos.dupterm` (standard on Pico).

---

## Protocol

Devices communicate with the Zelta cloud over MQTT or HTTPS:

```
Device → Cloud:
  zelta/{product_id}/{device_id}/up/status          # Status updates
  zelta/{product_id}/{device_id}/up/heartbeat       # Keep-alive (every 60s)
  zelta/{product_id}/{device_id}/up/check           # Check for OTA updates
  zelta/{product_id}/{device_id}/up/telemetry/*     # Sensor / telemetry data

Cloud → Device:
  zelta/{product_id}/{device_id}/down/command       # Remote commands
  zelta/{product_id}/{device_id}/down/firmware      # OTA firmware chunks
```

MQTT broker: `mqtt.zeltasoft.com:8883` (TLS)

---

## License

MIT — see [LICENSE](LICENSE).

The Zelta cloud platform, web dashboard, and management SDK are proprietary software.
