# @Time : 2024/3/5-下午4:10
# @Author : yyw@ustc
# @E-mail : yang0@mail.ustc.edu.cn
# @Github : https://github.com/ustcyyw
# @desc :

# python 3.6
import random
import time

from paho.mqtt import client as mqtt_client

# 免费的Broker
broker = 'broker.emqx.io'
port = 1883

client_id = "yyw_test_publisher"  # 设定唯一设备号，不设则mqtt随机生成
topic = "yyw_test_mqtt"  # 自定义一个Topic


# 连接函数
def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc):
        # flags是一个包含代理回复的标志的字典；
        # rc的值决定了连接成功或者不成功（0为成功）
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)  # 实例化对象
    client.on_connect = on_connect  # 设定回调函数，当Broker响应连接时，就会执行给定的函数
    client.connect(broker, port)  # 连接
    return client


# 定义发送信息的函数

def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)  # 指定信息的tpoic和信息内容，并发送
        # result: [0, 1]
        status = result[0]  # 解析响应内容
        if status == 0:  # 发送成功
            print(f"Send `{msg}` to topic `{topic}`")
        else:  # 发送失败
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


if __name__ == '__main__':
    publisher = connect_mqtt(client_id)  # 连接
    publisher.loop_start()  # 新线程loop
    publish(publisher)  # 发送