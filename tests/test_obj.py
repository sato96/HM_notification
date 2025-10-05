from HM_notification import Msg

def test_msg():
    message = Msg(service="test_service", urlBroker="mqtt://192.168.1.20:1883", text="Hello, World!", topicDef="/test/topic")
    resp = message.sendMsg()
    print(resp)
    return message

def test_to_dict():
    message = test_msg()
    message.text = "Updated text"
    resp = message.sendMsg(topic="/alertHum")
    print(resp)
    dict_repr = message.to_dict()
    print(dict_repr)
    return dict_repr

def dict_to_msg():
    dict_repr = test_to_dict()
    message = Msg.from_dict(dict_repr, urlBroker="mqtt://192.168.1.20:1883")
    print(message)
    return message


if __name__ == "__main__":
    dict_to_msg()