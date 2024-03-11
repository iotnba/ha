# @Time : 2024/3/5-下午4:41
# @Author : yyw@ustc
# @E-mail : yang0@mail.ustc.edu.cn
# @Github : https://github.com/ustcyyw
# @desc :

import json
from paho.mqtt import client as mqtt_client

# 免费的Broker
broker = "broker.emqx.io"
port = 1883

client_id = "yyw_test_subscriber"  # 设定唯一设备号，不设则mqtt随机生成
topic = "$sys/OSTx26punO/chengyan001/thing/property/set"  # 自定义一个Topic(网关属性设置订阅)
pubTopic = "$sys/OSTx26punO/chengyan001/thing/property/set_reply"  # 自定义一个Topic(网关属性设置响应)
returnMsg = {"id": "{id}", "code": 200, "msg": "success"}


# 连接函数
def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        # flags是一个包含代理回复的标志的字典；
        # rc的值决定了连接成功或者不成功（0为成功）
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION1, client_id
    )  # 实例化对象
    client.on_connect = (
        on_connect  # 设定回调函数，当Broker响应连接时，就会执行给定的函数
    )
    client.connect(broker, port)  # 连接
    return client


# 订阅函数，设定要订阅的Topic，以及设定接受信息后的回调函数
def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        # 先解析出id
        data = json.load(msg.payload.decode("utf-8"))
        id = data["id"]
        pubMsg = returnMsg.format(id=id)
        result = client.publish(pubTopic, pubMsg)  # 指定信息的tpoic和信息内容，并发送
        # result: [0, 1]
        status = result[0]  # 解析响应内容
        if status == 0:  # 发送成功
            print(f"Send `{msg}` to topic `{pubTopic}`")
        else:  # 发送失败
            print(f"Failed to send message to topic {pubTopic}")

    client.subscribe(topic)
    client.on_message = on_message


if __name__ == "__main__":
    subscriber = connect_mqtt(client_id)  # 连接
    subscribe(subscriber)  # 订阅设置
    # 网络阻塞，不断接受并调用回调函数处理结果，意味着代码会一直卡在这里接受，所以可以使用多线程来使用
    subscriber.loop_forever()
