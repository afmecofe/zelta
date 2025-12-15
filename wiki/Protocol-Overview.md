# Protocol Overview

Zelta uses a **simple, open protocol** that works over MQTT or HTTPS. Any device that can speak these protocols can integrate with the platform.

## Protocol Layers

```
┌─────────────────────────────────────┐
│   Application Layer (Your Code)    │
├─────────────────────────────────────┤
│   Zelta Protocol (JSON Messages)   │ ◄── This layer is open and documented
├─────────────────────────────────────┤
│   Transport (MQTT or HTTPS/REST)   │
├─────────────────────────────────────┤
│   Security (TLS 1.2/1.3)           │
└─────────────────────────────────────┘
```

## Transport Options

### Option 1: MQTT (Recommended for IoT Devices)

**Best for:** Constrained devices, low power, bidirectional communication

**Connection:**
```
Broker: mqtt.zeltasoft.com
Port: 8883 (MQTT over TLS)
Protocol: MQTT 3.1.1 or 5.0
Auth: Username (device_id) + Password (API key)
```

**Pros:**
- Lightweight (~20KB RAM)
- Built-in QoS and offline queuing
- Bidirectional (receive commands instantly)
- Persistent sessions
- Lower latency

**Cons:**
- Requires MQTT client library
- MQTT bridge infrastructure needed

### Option 2: HTTPS REST API (Alternative)

**Best for:** Devices with sufficient resources, cellular connections

**Endpoint:** `https://api.zeltasoft.com`

**Pros:**
- Direct connection to cloud (no bridge)
- Standard HTTP libraries
- Works through corporate firewalls
- Easy to debug

**Cons:**
- Higher RAM usage (~150KB for TLS)
- No bidirectional communication (must poll)
- Higher latency

## Message Format

All messages use **JSON payloads**. Examples:

### Heartbeat
```json
{
  "timestamp": 1708436800,
  "uptime": 3600,
  "rssi": -65,
  "battery": 87,
  "free_memory": 45000
}
```

### Telemetry
```json
{
  "timestamp": 1708436800,
  "type": "sensors",
  "data": {
    "temperature": 25.3,
    "humidity": 65.2,
    "pressure": 1013.25
  }
}
```

### Status Update
```json
{
  "status": "online",
  "firmware_version": "1.2.3",
  "hardware_version": "rev-b",
  "ip_address": "192.168.1.100"
}
```

## Communication Patterns

### 1. Device Registration (First Boot)

```
Device                          Cloud
   │                              │
   ├──── POST /provision ─────────►
   │     {device_id, product_id}  │
   │                              │
   ◄──── API Key ─────────────────┤
   │                              │
```

### 2. Heartbeat (Keep-Alive)

```
Device                          Cloud
   │                              │
   ├──── up/heartbeat ────────────►
   │     {timestamp, uptime...}   │
   │                              │
   │     (every 60 seconds)       │
```

### 3. Telemetry Reporting

```
Device                          Cloud
   │                              │
   ├──── up/telemetry/sensors ────►
   │     {temperature, humidity}  │
   │                              │
   ├──── up/telemetry/battery ────►
   │     {voltage, soc}           │
```

### 4. OTA Update Check

```
Device                          Cloud
   │                              │
   ├──── POST /check-update ──────►
   │     {device_id, version}     │
   │                              │
   ◄──── Update Available ────────┤
   │     {version, url, hash}     │
   │                              │
   ├──── GET /firmware-chunk/1 ───►
   ◄──── Binary Data ─────────────┤
   │                              │
   ├──── POST /report-status ─────►
   │     {status: "updated"}      │
```

### 5. Remote Commands (MQTT Only)

```
Device                          Cloud
   │                              │
   │     Subscribe to:            │
   ├──── down/command ────────────┤
   │                              │
   ◄──── Command ─────────────────┤
   │     {cmd: "reboot"}          │
   │                              │
   ├──── up/command-result ───────►
   │     {status: "success"}      │
```

## Data Types

### Telemetry Types

| Type | Description | Example Fields |
|------|-------------|----------------|
| `engine` | Engine metrics | rpm, coolant_temp_c, oil_pressure_psi |
| `fluids` | Fluid levels | engine_oil_pct, hydraulic_fluid_pct |
| `battery` | Battery data | voltage, soc_pct, alternator_voltage |
| `location` | GPS coordinates | latitude, longitude, altitude_m |
| `sensors` | Custom sensors | Any key-value pairs |
| `diagnostics` | Fault codes | fault_codes[], warning_codes[] |

### Status Values

- `online` - Device is connected and operational
- `offline` - Device is disconnected
- `updating` - Firmware update in progress
- `error` - Device encountered an error

## Security

### Authentication

**Option 1: API Key (Recommended)**
```
MQTT: Username = device_id, Password = api_key
HTTPS: Header "X-API-Key: your-api-key"
```

**Option 2: TLS Client Certificates**
```
MQTT: Client certificate in TLS handshake
HTTPS: Mutual TLS (mTLS)
```

### Encryption

- **Required**: TLS 1.2 or higher
- **Recommended**: TLS 1.3 with AES-256-GCM
- **Certificates**: Valid CA-signed certificates
- **Verification**: Always verify server certificates in production

## Rate Limits

| Operation | Limit | Window |
|-----------|-------|--------|
| Heartbeat | 1 msg/min | Per device |
| Telemetry | 60 msgs/min | Per device |
| Update Check | 10 checks/hour | Per device |
| Commands | 100 msgs/min | Per device |

## Error Handling

### MQTT Errors

- **Connection Refused**: Check broker address, port, credentials
- **Publish Failed**: Check QoS level, topic permissions
- **Subscription Failed**: Verify topic format, wildcards

### HTTPS Errors

- **401 Unauthorized**: Invalid API key
- **429 Too Many Requests**: Rate limit exceeded
- **503 Service Unavailable**: Cloud platform issue

### Recovery Strategies

1. **Exponential Backoff**: Wait longer between retries (1s, 2s, 4s, 8s...)
2. **Offline Queuing**: Store messages locally, send when reconnected
3. **Health Monitoring**: Track connection uptime, alert on failures

## Implementation Guidelines

### Minimum Implementation

To integrate with Zelta, your device **must**:

1. Authenticate with API key or certificate
2. Send heartbeats every 60 seconds
3. Report status changes (online/offline)
4. Handle firmware update flow (optional but recommended)

### Recommended Implementation

For production, also implement:

1. Telemetry reporting (at least one type)
2. OTA updates with rollback
3. Remote command handling
4. TLS certificate validation
5. Offline message queuing
6. Error recovery and retry logic

## Next Steps

- [MQTT Topics](MQTT-Topics) - Detailed topic structure
- [REST API](REST-API) - Complete API reference
- [Message Formats](Message-Formats) - JSON schema definitions
- [Integration Examples](Integration-Examples) - Code samples for various platforms
