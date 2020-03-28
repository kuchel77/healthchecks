"""Platform for Healthchecks integration."""
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity


SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_PING_URL): cv.string,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    ping_url = config.get(CONF_PING_URL)

    add_entities([HealthChecksSensor(ping_url=ping_url)])


class HealthChecksSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, ping_url):
        """Initialize the sensor."""
        self._previous_update = None
        self._ping_url = ping_url

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Health Checks'

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return DEFAULT_DEVICE_CLASS
    
    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._previous_update


    def update(self):
        """TODO Sent the data and check"""
        self._previous_update = False