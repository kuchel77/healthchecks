"""Platform for Healthchecks integration."""
from datetime import timedelta
import logging
import voluptuous as vol
from pyhealthchecks import healthchecks
from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import PLATFORM_SCHEMA
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

SCAN_INTERVAL = timedelta(minutes=5)

CONF_PING_URL = "ping_url"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_PING_URL): cv.string})

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    ping_url = config.get(CONF_PING_URL)

    session = async_get_clientsession(hass)

    health_check = healthchecks.HealthChecks(
        hass.loop, ping_url=ping_url, session=session
    )

    async_add_entities([HealthChecksBinarySensor(health_check=health_check)])


class HealthChecksBinarySensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, health_check):
        """ Initialize the sensor. """
        self._previous_update = False
        self._health_check = health_check

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Health Checks"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._previous_update

    @Throttle(SCAN_INTERVAL)
    async def async_update(self, **kwargs):
        """ Do an async http update """
        await self._health_check.update_connection()
        self._previous_update = self._health_check.status
