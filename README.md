# 🧩 Msg – JSON Notification Standardization Library for SmartHome Ecosystem

This library provides a Python class (`Msg`) that defines a **standardized JSON messaging format** for your SmartHome ecosystem.  
It supports text, images, and videos (Base64-encoded), as well as custom structured data payloads.  

---

## 🚀 Key Features

- ✅ Unified JSON structure for alerts and notifications  
- 📦 Supports **text**, **images**, and **videos**  
- 🔁 Direct conversion between **JSON** and **Python dicts**  
- 🧠 Seamless integration with MQTT brokers via `HM_requests`  
- 🔧 Flexible fields for message type, sender, and routing  

---

## 🧱 Message Structure

Each `Msg` instance represents an object structured as follows:

```json
{
  "serviceAlert": "service_name",
  "msg": {
    "img": "BASE64_IMAGE_DATA",
    "video": "BASE64_VIDEO_DATA",
    "text": "Message text content",
    "data": {
      "custom_field": "value"
    }
  },
  "sender": "SenderIdentifier",
  "flToSender": false,
  "msgType": "text"
}
```

---

## ⚙️ Installation

Copy the `msg.py` file into your local library or project directory, then import the class:

```python
from msg import Msg
```

Make sure you have the dependency installed:
```bash
pip install HM_requests
```

---

## 💡 Basic Usage

### Creating a text message

```python
msg = Msg(
    service="temperature_monitor",
    urlBroker="mqtt://192.168.1.10:1883",
    text="Temperature too high!",
    sender="sensor_kitchen",
    msgType="text"
)

print(msg.to_json())
```

### Adding an image or video

```python
msg = Msg(
    service="camera_alert",
    urlBroker="mqtt://192.168.1.10:1883",
    imgPath="/home/user/capture.jpg",
    text="Motion detected in the living room",
    sender="camera_livingroom",
    msgType="image"
)
```

---

## 🔄 Conversion & Parsing

### From a Python dict

```python
msg_dict = {
    "serviceAlert": "door_sensor",
    "msg": {"text": "Front door opened"},
    "sender": "sensor_entrance"
}

msg = Msg.from_dict(msg_dict, urlBroker="mqtt://192.168.1.10:1883")
```

### From a JSON string

```python
msg_json = '{"serviceAlert": "garage_sensor", "msg": {"text": "Door closed"}, "sender": "sensor_garage"}'
msg = Msg.from_json(msg_json, urlBroker="mqtt://192.168.1.10:1883")
```

---

## 📤 Sending a Message via MQTT

To send the message to the MQTT broker:

```python
result = msg.sendMsg("/alert/garage")
print(result)
```

If no topic is provided, the default topic (`/alert`) will be used.

---

## 🧩 Main Properties

| Property        | Type       | Description |
|-----------------|------------|-------------|
| `broker`        | `str`      | MQTT broker URL |
| `service`       | `str`      | Service or module generating the message |
| `text`          | `str`      | Text content |
| `img`           | `str` (Base64) | Base64-encoded image |
| `video`         | `str` (Base64) | Base64-encoded video |
| `data`          | `dict`     | Custom structured data |
| `sender`        | `str`      | Sender identifier |
| `fl_to_sender`  | `bool`     | If `True`, responses are routed back to the sender |
| `msgType`       | `str`      | Message type (`text`, `image`, `video`, etc.) |

---

## 🧠 Implementation Notes

- Files are automatically encoded to **Base64** before being inserted in the JSON payload.  
- MQTT communication is abstracted through `Request.post()` from the `HM_requests` module.  
- Topics are normalized to always start with `/`.  

---

## 📜 License

This project is distributed under the **MIT License**.  
You are free to use, modify, and integrate it into your home or industrial ecosystem.  
