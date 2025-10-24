import base64
import json
from urllib.parse import urlparse
from HM_requests import Request

class Msg(object):
    ## Constructor
    """
    Message structure:
    {
        "serviceAlert": self._service,    # Service identifier for the alert
        "msg": {
            "img": self._img,            # Base64 encoded image if present
            "video": self._video,        # Base64 encoded video if present
            "text": self._text,          # Text message content
            "data": self._data           # Additional custom data payload
        },
        "sender": self._sender,          # Identifier of the message sender
        "flToSender": self._flToSender,  # Flag indicating if response should be sent back to sender
        "msgType": self._msgType         # Type of message (e.g., "text", "image", "video")
    }
    """

    def __init__(self, service, urlBroker, topicDef=None, imgPath=None, videoPath=None, text=None, data=None, sender = None, flToSender=False, msgType=None):
        self._broker = urlBroker
        self._topicDef = topicDef if topicDef is not None else "/alert"
        self._topicDef = self._topicDef if self._topicDef.startswith("/") else "/" + self._topicDef
        self._service = service
        self._img = self._encode_to_base64(imgPath) if imgPath is not None else None
        self._video = self._encode_to_base64(videoPath) if videoPath is not None else None
        self._text = text
        self._data = data
        self._flToSender = flToSender
        self._sender = sender
        self._msgType = msgType if msgType is not None else "text"

    @classmethod
    def from_dict(cls, data, urlBroker, topicDef=None):
        """Create a Msg object from a dictionary.
        
        Args:
            data (dict): Dictionary in the same format as to_dict() output
            urlBroker (str): MQTT broker URL
        
        Returns:
            Msg: New Msg instance
        """
        msg = cls(
            service=data.get('serviceAlert'),
            urlBroker=urlBroker,
            sender=data.get('sender'),
            flToSender=data.get('flToSender', False),
            topicDef=topicDef
        )
        
        # Handle nested msg dictionary
        msg_data = data.get('msg', {})
        msg._img = msg_data.get('img')
        msg._video = msg_data.get('video')
        msg._text = msg_data.get('text')
        msg._data = msg_data.get('data')
        msg._flToSender = data.get('flToSender', False)
        msg._sender = data.get('sender')
        msg._service = data.get('serviceAlert')
        msg._msgType = data.get('msgType', 'text')
        
        return msg
    

    @classmethod
    def from_json(cls, json_str, urlBroker, topicDef=None):
        """Create a Msg object from a JSON string.
        
        Args:
            json_str (str): JSON string in the same format as to_json() output
            urlBroker (str): MQTT broker URL
        
        Returns:
            Msg: New Msg instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data, urlBroker, topicDef)


  # Getters
    @property
    def broker(self):
        return self._broker

    @property
    def msgType(self):
        return self._msgType

    @property
    def topic_def(self):
        return self._topicDef
    
    @property
    def service(self):
        return self._service
    
    @property
    def img(self):
        return self._img
    
    @property
    def video(self):
        return self._video
    
    @property
    def text(self):
        return self._text
    
    @property
    def data(self):
        return self._data
    
    @property
    def fl_to_sender(self):
        return self._flToSender

    @property
    def sender(self):
        return self._sender

    # Setters
    @broker.setter
    def broker(self, value):
        self._broker = value
    
    @topic_def.setter
    def topic_def(self, value):
        self._topicDef = value if value is not None else "/alert"
    
    @service.setter
    def service(self, value):
        self._service = value

    @img.setter
    def img(self, value):
        self._img = self._encode_to_base64(value) if value is not None else None

    @video.setter
    def video(self, value):
        self._video = self._encode_to_base64(value) if value is not None else None
    
    @text.setter
    def text(self, value):
        self._text = value
    
    @data.setter
    def data(self, value):
        self._data = value
    @sender.setter
    def sender(self, value):
        self._sender = value 

    @fl_to_sender.setter
    def fl_to_sender(self, value):
        self._flToSender = value

    @msgType.setter
    def msgType(self, value):
        self._msgType = value

    def to_dict(self):
            return {
                "serviceAlert": self._service,
                "msg":{
                    "img": self._img,
                    "video": self._video,
                    "text": self._text,
                    "data": self._data
                },
                "sender": self._sender,
                "flToSender": self._flToSender,
                "msgType": self._msgType
            }
    
    def to_json(self):
            return json.dumps(self.to_dict())

# Function to read and encode file in Base64
    def _encode_to_base64(self,file_path):
        with open(file_path, "rb") as file:
            encoded_file = base64.b64encode(file.read()).decode("utf-8")
        return encoded_file

    def sendMsg(self, topic = None):
        if topic is None:
            topic = self._topicDef
        else:
            topic = topic if topic.startswith("/") else "/" + topic
        payload = self.to_json()
        url = "mqtt://" + urlparse(self._broker).hostname + ":" + str(urlparse(self._broker).port) + topic
        req = Request.post(url, payload=payload, topic = topic)
        return req