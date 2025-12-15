# MQTT Transport Protocol

Zelta uses MQTT as the primary transport protocol for embedded devices due to its efficiency and reliability.

## Overview

MQTT (Message Queuing Telemetry Transport) is designed for constrained devices and low-bandwidth networks. Key benefits:

- **Lightweight**: ~20KB RAM footprint vs ~150KB for HTTPS
- **Reliable**: Built-in QoS levels and persistent sessions
- **Bidirectional**: Publish/Subscribe enables real-time commands
- **Efficient**: Binary protocol with minimal overhead
- **Resilient**: Automatic reconnection and message queuing

## Connection Parameters

```c
Broker: mqtt.zeltasoft.com
Port: 8883 (MQTT over TLS)
Protocol: MQTT 3.1.1 or 5.0
TLS: Required (TLS 1.2 or 1.3)
Authentication: Username/Password or Client Certificate
Keep-Alive: 60 seconds (configurable)
Clean Session: False (for persistent sessions)
```

## Topic Structure

All Zelta MQTT topics follow this pattern:

```
zelta/{product_id}/{device_id}/{direction}/{category}[/{subcategory}]
```

### Device → Cloud (Upstream)

Devices publish to `up/` topics:

| Topic | Purpose | QoS | Retained |
|-------|---------|-----|----------|
| `up/heartbeat` | Keep-alive ping | 0 | No |
| `up/status` | Device status updates | 1 | Yes |
| `up/telemetry/engine` | Engine metrics | 1 | No |
| `up/telemetry/battery` | Battery data | 1 | No |
| `up/telemetry/location` | GPS coordinates | 1 | No |
| `up/telemetry/sensors` | Custom sensor data | 1 | No |
| `up/check` | OTA update check | 1 | No |
| `up/logs` | Device logs | 0 | No |

### Cloud → Device (Downstream)

Devices subscribe to `down/` topics:

| Topic | Purpose | QoS |
|-------|---------|-----|
| `down/command` | Remote commands | 1 |
| `down/response` | Command responses | 1 |
| `down/firmware` | OTA firmware chunks | 2 |
| `down/config` | Configuration updates | 1 |

## Quality of Service (QoS)

### QoS 0 - At Most Once
- Fire and forget
- No acknowledgment
- Use for: Heartbeats, logs, non-critical telemetry

### QoS 1 - At Least Once
- Guaranteed delivery with acknowledgment
- Possible duplicates
- **Recommended for telemetry**

### QoS 2 - Exactly Once
- Guaranteed delivery, no duplicates
- Higher overhead
- Use for: Firmware updates, critical commands

## Message Formats

### Heartbeat
```json
{
  "timestamp": 1708436800,
  "uptime": 3600,
  "rssi": -65,
  "battery": 87
}
```

### Status Update
```json
{
  "status": "online",
  "firmware_version": "1.2.3",
  "sdk_version": "1.0.0",
  "free_memory": 45000,
  "ip_address": "192.168.1.100"
}
```

### Telemetry
```json
{
  "timestamp": 1708436800,
  "values": {
    "temperature": 25.3,
    "humidity": 65.2,
    "pressure": 1013.25
  }
}
```

### Command (Cloud → Device)
```json
{
  "command_id": "cmd-123",
  "type": "reboot",
  "params": {
    "delay_seconds": 10
  }
}
```

### Command Response (Device → Cloud)
```json
{
  "command_id": "cmd-123",
  "status": "success",
  "result": {
    "executed_at": 1708436810
  }
}
```

## Configuration

### Kconfig Options

```ini
# Enable MQTT transport
CONFIG_ZELTA_TRANSPORT_MQTT=y

# Broker settings
CONFIG_ZELTA_MQTT_BROKER="mqtt.zeltasoft.com"
CONFIG_ZELTA_MQTT_PORT=8883

# TLS/Security
CONFIG_ZELTA_TLS_ENABLED=y
CONFIG_ZELTA_TLS_VERIFY_PEER=y

# Connection parameters
CONFIG_ZELTA_MQTT_KEEPALIVE=60
CONFIG_ZELTA_MQTT_QOS_TELEMETRY=1
CONFIG_ZELTA_MQTT_CLEAN_SESSION=n

# Buffer sizes
CONFIG_ZELTA_MQTT_TX_BUFFER_SIZE=1024
CONFIG_ZELTA_MQTT_RX_BUFFER_SIZE=1024
```

## Code Example

```c
#include <zelta/mqtt.h>

void main(void) {
    struct zelta_mqtt_config cfg = {
        .broker = "mqtt.zeltasoft.com",
        .port = 8883,
        .client_id = "device-abc123",
        .username = "device-abc123",
        .password = "api-key-secret",
        .use_tls = true,
        .keepalive = 60,
        .clean_session = false,
    };
    
    // Connect
    zelta_mqtt_connect(&cfg);
    
    // Subscribe to commands
    zelta_mqtt_subscribe("down/command", on_command_received);
    
    // Publish telemetry
    char payload[256];
    snprintf(payload, sizeof(payload), 
             "{\"temperature\":%.1f}", sensor_read_temp());
    zelta_mqtt_publish("up/telemetry/sensors", payload, 1, false);
    
    // Process messages
    while (1) {
        zelta_mqtt_loop();
        k_sleep(K_MSEC(100));
    }
}

void on_command_received(const char *topic, const char *payload) {
    printk("Received command: %s\n", payload);
    // Parse and execute command
}
```

## Last Will and Testament (LWT)

Automatically notify the cloud when a device disconnects unexpectedly:

```c
struct zelta_mqtt_lwt lwt = {
    .topic = "up/status",
    .payload = "{\"status\":\"offline\",\"reason\":\"unexpected\"}",
    .qos = 1,
    .retain = true,
};
zelta_mqtt_set_lwt(&lwt);
```

## Persistent Sessions

For devices with intermittent connectivity:

```c
// Set clean_session = false to maintain subscriptions
cfg.clean_session = false;

// Cloud will queue messages while device is offline
// Messages delivered when device reconnects
```

## Best Practices

1. **Use QoS 1 for telemetry** - Balances reliability and overhead
2. **Enable persistent sessions** - For mobile/intermittent devices
3. **Set appropriate keep-alive** - 60s typical, 300s for slow networks
4. **Implement exponential backoff** - On reconnection failures
5. **Validate TLS certificates** - Always verify peer in production
6. **Batch telemetry** - Send multiple readings in one message
7. **Use retained messages** - For device status, last known state
8. **Monitor connection state** - Handle disconnects gracefully

## Troubleshooting

**Connection refused**
- Check broker address and port
- Verify credentials (username/API key)
- Ensure TLS is configured correctly

**Messages not delivered**
- Check QoS level
- Verify topic permissions
- Monitor broker logs

**Frequent disconnects**
- Increase keep-alive interval
- Check network stability
- Review power management settings

**High latency**
- Reduce keep-alive interval
- Use QoS 0 for non-critical data
- Check network conditions

## See Also

- [TLS Security](TLS-Security)
- [MQTT Topics](MQTT-Topics)
- [Telemetry API](API-Telemetry)
- [Command Handling](Command-Handling)
