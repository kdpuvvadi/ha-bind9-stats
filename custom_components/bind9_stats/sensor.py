from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DOMAIN


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the BIND9 sensors linked to the coordinator."""
    coordinator = hass.data[DOMAIN]

    # Definitions mapping target JSON path to entity configurations
    sensor_types = [
        {
            "name": "BIND9 Version",
            "keys": ["version"],
            "icon": "mdi:dns",
            "state_class": None,
            "unit": None,
        },
        {
            "name": "BIND9 Total Queries",
            "keys": ["opcodes", "QUERY"],
            "icon": "mdi:comment-question-outline",
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "unit": "queries",
        },
        {
            "name": "BIND9 Success Responses",
            "keys": ["rcodes", "NOERROR"],
            "icon": "mdi:check-circle-outline",
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "unit": "responses",
        },
        {
            "name": "BIND9 NXDOMAIN Responses",
            "keys": ["rcodes", "NXDOMAIN"],
            "icon": "mdi:alert-circle-outline",
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "unit": "responses",
        },
        {
            "name": "BIND9 SERVFAIL Responses",
            "keys": ["rcodes", "SERVFAIL"],
            "icon": "mdi:close-circle-outline",
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "unit": "responses",
        },
        {
            "name": "BIND9 Cache Hits",
            "keys": ["views", "_default", "resolver", "cachestats", "CacheHits"],
            "icon": "mdi:cached",
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "unit": "hits",
        },
        {
            "name": "BIND9 Cache Misses",
            "keys": ["views", "_default", "resolver", "cachestats", "CacheMisses"],
            "icon": "mdi:cached",
            "state_class": SensorStateClass.TOTAL_INCREASING,
            "unit": "misses",
        },
    ]

    entities = [BIND9Sensor(coordinator, s) for s in sensor_types]
    async_add_entities(entities)


class BIND9Sensor(CoordinatorEntity, SensorEntity):
    """Representation of individual BIND9 metrics."""

    def __init__(self, coordinator, sensor_def):
        super().__init__(coordinator)
        self._name = sensor_def["name"]
        self._keys = sensor_def["keys"]
        self._attr_icon = sensor_def["icon"]
        self._attr_state_class = sensor_def["state_class"]
        self._attr_native_unit_of_measurement = sensor_def["unit"]
        self._attr_unique_id = f"bind9_{'_'.join(self._keys).lower()}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        """Navigate through nested keys securely."""
        val = self.coordinator.data
        if not val:
            return None
        for key in self._keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return None
        return val
