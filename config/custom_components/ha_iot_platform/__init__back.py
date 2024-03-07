"""ha对接物联网平台测试插件."""
import logging

from homeassistant.const import MATCH_ALL
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers.typing import ConfigType

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "ha_iot_platform"

# HA的restful服务地址，除非自定义了端口，一般不用改
HA_REST_URL = "http://127.0.0.1:8123"

_LOGGER = logging.getLogger()


class HaIotPlatform:
    async def handle_ha_event(self, event: Event) -> None:
        print(event)
        _LOGGER.warning(event)
        _LOGGER.warning("test!!!!!!!!!!!!!!!!!!!!!!!!!!")


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """The init entry for HA."""

    hip = HaIotPlatform()

    # listen to events
    hass.bus.async_listen(MATCH_ALL, hip.handle_ha_event)

    # Return boolean to indicate that initialization was successfully.
    return True
