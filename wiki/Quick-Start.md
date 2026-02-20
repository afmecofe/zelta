# Quick Start Guide

Get your first device connected to Zelta in 15 minutes. **Choose your platform** below.

## Choose Your Path

- **[Raspberry Pi / Linux PC](#quick-start-linux)** - Easiest, 5 minutes
- **[ESP32 with Arduino](#quick-start-arduino)** - For Arduino developers
- **[Zephyr RTOS](#quick-start-zephyr)** - For embedded RTOS projects
- **[Python / MicroPython](#quick-start-python)** - Rapid prototyping
- **[Any other platform](#quick-start-custom)** - Use the protocol directly

---

## Quick Start: Linux (Raspberry Pi, Ubuntu, etc.)

**Time: 5 minutes** | **Difficulty: Easy**

### 1. Create Account & Get Credentials

1. Sign up at https://app.zeltasoft.com
2. Create an organization
3. Add a device → Copy **API key** and **device ID**

### 2. Install Zelta Agent

```bash
# Download and install
curl -sSL https://github.com/afmecofe/zelta/releases/latest/download/install.sh | bash

# Or build from source
git clone https://github.com/afmecofe/zelta.git
cd zelta && mkdir build && cd build
cmake .. && make
sudo make install
```

### 3. Configure

```bash
# Edit config
sudo nano /etc/zelta/config.json
```

```json
{
  "device_id": "your-device-id",
  "product_id": "your-product-id",
  "api_key": "your-api-key",
  "mqtt_broker": "mqtt.zeltasoft.com",
  "mqtt_port": 8883
}
```

### 4. Start Service

```bash
sudo systemctl enable zelta-agent
sudo systemctl start zelta-agent
sudo systemctl status zelta-agent
```

### 5. Verify

```bash
# Check logs
journalctl -u zelta-agent -f

# You should see:
# [INFO] Connected to mqtt.zeltasoft.com:8883
# [INFO] Device online: device-abc123
```

✅ **Done!** Check your dashboard at https://app.zeltasoft.com

---

## Quick Start: Python

**Time: 10 minutes** | **Difficulty: Easy**

Perfect for Raspberry Pi, Linux PCs, or prototyping.

### 1. Install Dependencies

```bash
pip install paho-mqtt requests
```

### 2. Create `zelta_client.py`

```python
import paho.mqtt.client as mqtt
import json
import time

# Configuration (get from dashboard)
DEVICE_ID = "your-device-id"
PRODUCT_ID = "your-product-id"
API_KEY = "your-api-key"
BROKER = "mqtt.zeltasoft.com"
PORT = 8883

def on_connect(client, userdata, flags, rc):
    print(f"Connected: {rc}")
    # Subscribe to commands
    client.subscribe(f"zelta/{PRODUCT_ID}/{DEVICE_ID}/down/command")

def on_message(client, userdata, msg):
    print(f"Command: {msg.payload.decode()}")

# Connect
client = mqtt.Client()
client.username_pw_set(DEVICE_ID, API_KEY)
client.tls_set()  # Enable TLS
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

# Send telemetry
while True:
    payload = json.dumps({
        "temperature": 25.3,
        "humidity": 60.0
    })
    topic = f"zelta/{PRODUCT_ID}/{DEVICE_ID}/up/telemetry/sensors"
    client.publish(topic, payload, qos=1)
    print(f"Sent: {payload}")
    time.sleep(60)
```

### 3. Run

```bash
python3 zelta_client.py
```

✅ **Done!** View data in dashboard.

---

## Quick Start: Arduino (ESP32)

**Time: 10 minutes** | **Difficulty: Moderate**

### 1. Install Libraries

In Arduino IDE:
- Sketch → Include Library → Manage Libraries
- Install: **PubSubClient**, **ArduinoJson**

### 2. Create Sketch

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// WiFi credentials
const char* ssid = "your-wifi-ssid";
const char* password = "your-wifi-password";

// Zelta credentials
const char* deviceId = "your-device-id";
const char* productId = "your-product-id";
const char* apiKey = "your-api-key";
const char* mqttServer = "mqtt.zeltasoft.com";

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  espClient.setInsecure(); // For testing, use proper certs in production
  client.setServer(mqttServer, 8883);
  
  // Connect to MQTT
  while (!client.connect(deviceId, deviceId, apiKey)) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("Connected!");
}

void loop() {
  client.loop();
  
  // Send telemetry every 60 seconds
  StaticJsonDocument<200> doc;
  doc["temperature"] = 25.3;
  doc["humidity"] = 60.0;
  
  char buffer[256];
  serializeJson(doc, buffer);
  
  String topic = "zelta/" + String(productId) + "/" + String(deviceId) + "/up/telemetry/sensors";
  client.publish(topic.c_str(), buffer, 1);
  
  delay(60000);
}
```

### 3. Upload & Monitor

Upload code → Open Serial Monitor

✅ **Done!** Device is now online.

---

## Quick Start: Zephyr RTOS

**Time: 30 minutes** | **Difficulty: Advanced**

For professional embedded development.

### 1. Install Zephyr

```bash
# Follow: https://docs.zephyrproject.org/latest/develop/getting_started/
pip3 install west
west init ~/zephyrproject
cd ~/zephyrproject
west update
```

### 2. Clone Zelta

```bash
cd ~/zephyrproject
git clone --recursive https://github.com/didavie/Zelta.git
cd Zelta/embedded
```

### 3. Configure

Edit `samples/basic_telemetry/prj.conf`:

```ini
CONFIG_ZELTA_PRODUCT_ID="your-product-id"
CONFIG_ZELTA_DEVICE_ID="your-device-id"
CONFIG_ZELTA_API_KEY="your-api-key"
CONFIG_ZELTA_MQTT_BROKER="mqtt.zeltasoft.com"
```

### 4. Build & Flash

```bash
west build -b esp32_devkitc_wrover samples/basic_telemetry
west flash
west attach
```

✅ **Done!** Professional embedded development.

---

## Quick Start: Custom Platform

**Time: Varies** | **Any platform with MQTT or HTTPS**

### Using MQTT (Recommended)

```bash
# Test with mosquitto_pub
mosquitto_pub -h mqtt.zeltasoft.com -p 8883 \
  --capath /etc/ssl/certs \
  -u "your-device-id" \
  -P "your-api-key" \
  -t "zelta/product-id/device-id/up/telemetry/sensors" \
  -m '{"temperature":25.3}' \
  -q 1
```

### Using HTTPS (Alternative)

```bash
# Test with curl
curl -X POST https://api.zeltasoft.com/report-telemetry \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "your-device-id",
    "type": "sensors",
    "data": {"temperature": 25.3}
  }'
```

✅ See [Protocol Overview](Protocol-Overview) for full implementation guide.

---

## Next Steps

After getting your first device connected:

- [Send Different Telemetry Types](Telemetry-Types) - Engine, battery, location
- [Implement OTA Updates](OTA-Updates) - Remote firmware updates
- [Handle Commands](Command-Handling) - Control devices remotely
- [Optimize Power](Power-Management) - For battery devices
- [Production Checklist](Production-Checklist) - Security and reliability

## Troubleshooting

### Connection Issues

**MQTT connection refused**
- Verify broker address: `mqtt.zeltasoft.com:8883`
- Check API key is correct
- Ensure TLS is enabled

**Certificate errors**
- Update system CA certificates: `sudo update-ca-certificates`
- Verify server: `openssl s_client -connect mqtt.zeltasoft.com:8883`

### No Data in Dashboard

**Device shows offline**
- Send heartbeat every 60 seconds
- Check topic format: `zelta/{product_id}/{device_id}/up/heartbeat`

**Telemetry not appearing**
- Verify topic: `zelta/{product_id}/{device_id}/up/telemetry/{type}`
- Check JSON format is valid
- Ensure QoS is 1 (not 0)

### Authentication

**401 Unauthorized**
- Verify API key in dashboard
- Check device is registered
- Ensure product_id matches

## Support

- **Wiki**: Complete documentation here
- **GitHub Issues**: https://github.com/afmecofe/zelta/issues
- **Discussions**: https://github.com/afmecofe/zelta/discussions
- **Email**: support@zeltasoft.com
