# HM_notification

A Python library for sending notifications across MQTT brokers with support for text, images, videos, and custom data.

## Features

- Send notifications with:
  - Text messages
  - Base64 encoded images
  - Base64 encoded videos 
  - Custom data payloads
- MQTT broker integration
- Flexible topic management
- Service identification
- Sender tracking capability

## Installation

Install using pip directly from GitHub:

```sh
pip install git+https://github.com/your-username/HM_notification.git
```

## Dependencies

- HM_requests (custom request library for protocol handling)
- Python 3.10+

## Usage

Basic example:

```python
from HM_notification import Msg

# Create a notification
notification = Msg(
    service="my_service",
    urlBroker="mqtt://localhost:1883",
    text="Hello World!",
    sender="service_1"
)

# Send the notification
notification.sendMsg()
```

Advanced example with image:

```python
from HM_notification import Msg

notification = Msg(
    service="camera_service",
    urlBroker="mqtt://broker.example.com:1883",
    topicDef="/cameras/alerts",
    imgPath="/path/to/image.jpg",
    text="Motion detected!",
    data={"timestamp": "2024-02-10 15:30:00"},
    sender="camera_1"
)

# Send to custom topic
notification.sendMsg(topic="/cameras/motion")
```

## API Reference

### Msg Class

#### Constructor

```python
Msg(service, urlBroker, topicDef=None, imgPath=None, videoPath=None, text=None, data=None, sender=None, flToSender=False)
```

Parameters:
- `service`: Service identifier
- `urlBroker`: MQTT broker URL
- `topicDef`: Default topic (defaults to "/alert")
- `imgPath`: Path to image file
- `videoPath`: Path to video file
- `text`: Text message
- `data`: Custom data payload
- `sender`: Sender identifier
- `flToSender`: Flag for sender-specific behavior

#### Methods

- `sendMsg(topic=None)`: Send the notification (uses default topic if none specified)
- `to_dict()`: Convert notification to dictionary
- `to_json()`: Convert notification to JSON string

#### Properties

All fields are accessible through getters and setters:
- `broker`
- `topic_def`
- `service`
- `img`
- `video`
- `text`
- `data`
- `sender`
- `fl_to_sender`

## License

MIT License