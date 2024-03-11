"""
ha对接物联网平台测试插件
"""
import logging

from homeassistant.const import MATCH_ALL
from homeassistant.core import (
    HomeAssistant,
    Event,
)
from homeassistant.helpers.typing import ConfigType

from .publisher import connect_mqtt


# The domain of your component. Should be equal to the name of your component.
DOMAIN = "ha_iot_platform"

# HA的restful服务地址，除非自定义了端口，一般不用改
HA_REST_URL = "http://127.0.0.1:8123"

client_id = "yyw_test_publisher"  # 设定唯一设备号，不设则mqtt随机生成
topic = "$sys/OSTx26punO/chengyan001/thing/property/post"  # 自定义一个Topic

_LOGGER = logging.getLogger()


class HaIotPlatform:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.loop_start()  # 新线程loop

    async def handle_ha_event(self, event: Event) -> None:
        _LOGGER.warning("test!!!!!!!!!!!!!!!!!!!!!!!!!!")
        msg = {"id": "1000", "version": "1.0", "params": {"DeviceNum": {"value": 1}}}
        result = self.publisher.publish(topic, msg)  # 指定信息的tpoic和信息内容，并发送
        # result: [0, 1]
        status = result[0]  # 解析响应内容
        if status == 0:  # 发送成功
            print(f"Send `{msg}` to topic `{topic}`")
        else:  # 发送失败
            print(f"Failed to send message to topic {topic}")


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """The init entry for HA."""
    hip = HaIotPlatform(connect_mqtt(client_id))

    # listen to events
    hass.bus.async_listen(MATCH_ALL, hip.handle_ha_event)

    # Return boolean to indicate that initialization was successfully.
    return True
