from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from . import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the BIND9 sensors linked to a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensor_types = [
        {"name": "BIND9 Version", "keys": ["version"], "icon": "mdi:dns", "state_class": None, "unit": None},
        {"name": "BIND9 Total Queries", "keys": ["opcodes", "QUERY"], "icon": "mdi:comment-question-outline", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "queries"},
        {"name": "BIND9 Success Responses", "keys": ["rcodes", "NOERROR"], "icon": "mdi:check-circle-outline", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "responses"},
        {"name": "BIND9 NXDOMAIN Responses", "keys": ["rcodes", "NXDOMAIN"], "icon": "mdi:alert-circle-outline", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "responses"},
        {"name": "BIND9 SERVFAIL Responses", "keys": ["rcodes", "SERVFAIL"], "icon": "mdi:close-circle-outline", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "responses"},
        {"name": "BIND9 Query Type A", "keys": ["qtypes", "A"], "icon": "mdi:alpha-a-box-outline", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "queries"},
        {"name": "BIND9 Query Type AAAA", "keys": ["qtypes", "AAAA"], "icon": "mdi:alpha-a-box", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "queries"},
        {"name": "BIND9 Query Type PTR", "keys": ["qtypes", "PTR"], "icon": "mdi:map-marker-path", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "queries"},
        {"name": "BIND9 Cache Hits", "keys": ["views", "_default", "resolver", "cachestats", "CacheHits"], "icon": "mdi:cached", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "hits"},
        {"name": "BIND9 Cache Misses", "keys": ["views", "_default", "resolver", "cachestats", "CacheMisses"], "icon": "mdi:cached", "state_class": SensorStateClass.TOTAL_INCREASING, "unit": "misses"},
    ]
    
    entities = [BIND9Sensor(coordinator, entry, s) for s in sensor_types]
    async_add_entities(entities)

class BIND9Sensor(CoordinatorEntity, SensorEntity):
    """Representation of individual BIND9 metrics."""

    def __init__(self, coordinator, entry, sensor_def):
        super().__init__(coordinator)
        self._entry = entry
        self._name = sensor_def["name"]
        self._keys = sensor_def["keys"]
        self._attr_icon = sensor_def["icon"]
        self._attr_state_class = sensor_def["state_class"]
        self._attr_native_unit_of_measurement = sensor_def["unit"]
        self._attr_unique_id = f"{entry.entry_id}_{'_'.join(self._keys).lower()}"

    @property
    def name(self):
        return self._name

    @property
    def native_value(self):
        val = self.coordinator.data
        if not val:
            return None
        for key in self._keys:
            if isinstance(val, dict) and key in val:
                val = val[key]
            else:
                return None
        return val

    @property
    def device_info(self) -> DeviceInfo:
        """Link this entity to a central BIND9 Device entry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=f"BIND9 Server ({self._entry.data['host']})",
            manufacturer="ISC",
            model="BIND9 DNS Server",
            # Dynamically grab the version string from the data payload if available
            sw_version=self.coordinator.data.get("version") if self.coordinator.data else None,
        )