# @Time : 2024/3/5-下午4:41
# @Author : yyw@ustc
# @E-mail : yang0@mail.ustc.edu.cn
# @Github : https://github.com/ustcyyw
# @desc :


from paho.mqtt import client as mqtt_client

# 免费的Broker
broker = 'broker.emqx.io'
port = 1883

client_id = "yyw_test_subscriber"  # 设定唯一设备号，不设则mqtt随机生成
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


# 订阅函数，设定要订阅的Topic，以及设定接受信息后的回调函数
def subscribe(client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


if __name__ == '__main__':
    subscriber = connect_mqtt(client_id)  # 连接
    subscribe(subscriber)  # 订阅设置
    # 网络阻塞，不断接受并调用回调函数处理结果，意味着代码会一直卡在这里接受，所以可以使用多线程来使用
    subscriber.loop_forever()