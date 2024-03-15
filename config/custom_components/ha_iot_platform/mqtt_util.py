# @Time : 2024/3/5-下午4:10
# @Author : yyw@ustc
# @E-mail : yang0@mail.ustc.edu.cn
# @Github : https://github.com/ustcyyw
# @desc :

# python 3.6
import logging
import json
import ssl
from . import generator_signature
from paho.mqtt import client as mqtt_client


subTopic = "$sys/OSTx26punO/chengyan001/thing/property/set"  # 自定义一个Topic(网关属性设置订阅)
pubTopic = "$sys/OSTx26punO/chengyan001/thing/property/set_reply"  # 自定义一个Topic(网关属性设置响应)
returnMsg = '{"id": "{id}", "code": 200, "msg": "success"}'

_LOGGER = logging.getLogger()


# 连接函数
def connect_mqtt(config):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        _LOGGER.error(
            f"--------------------Received `{msg.payload.decode()}` from `{msg.topic}` topic"
        )

        # 先解析出id
        data = json.loads(msg.payload.decode())
        id = data["id"]
        # ha收到物联网平台的下方消息 再次回复 现在是写死的
        pubMsg = returnMsg.format(id=id)
        result = client.publish(pubTopic, pubMsg)  # 指定信息的tpoic和信息内容，并发送
        # result: [0, 1]
        status = result[0]  # 解析响应内容
        if status == 0:  # 发送成功
            print(f"Send `{msg}` to topic `{pubTopic}`")
        else:  # 发送失败
            print(f"Failed to send message to topic {pubTopic}")

    def on_connect(client, userdata, flags, rc):
        # flags是一个包含代理回复的标志的字典；
        # rc的值决定了连接成功或者不成功（0为成功）
        if rc == 0:
            logging.error("--------------------------Connected to MQTT Broker!")
        else:
            logging.error(
                "--------------------------Failed to connect, return code %d\n", rc
            )
        client.subscribe(subTopic)
        client.on_message = on_message

    try:
        # 读取配置文件
        mqtt_client_id = config.get("mqtt_client_id")
        mqtt_username = config.get("mqtt_username")
        version = config.get("version")
        resourcename = config.get("resourcename")
        accessKey = config.get("accessKey")
        mqtt_port = config.get("mqtt_port")
        mqtt_broker = config.get("mqtt_broker")
        mqtt_password = generator_signature.assemble_token(
            version, resourcename, accessKey
        )

        client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, mqtt_client_id
        )  # 实例化对象
        client.on_connect = (
            on_connect  # 设定回调函数，当Broker响应连接时，就会执行给定的函数
        )
        # 设置用户名和密码
        client.username_pw_set(username=mqtt_username, password=mqtt_password)
        client.tls_set(cert_reqs=ssl.CERT_NONE)
        client.connect(mqtt_broker, mqtt_port)  # 连接
        return client
    except Exception as e:
        logging.error("mqtt connect error!!!!!!!!!!")
        logging.error(e)
        raise e
