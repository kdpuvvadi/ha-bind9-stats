import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

DOMAIN = "bind9_stats"
_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BIND9 Statistics from a config entry."""
    host = entry.data["host"]

    coordinator = BIND9Coordinator(hass, host)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class BIND9Coordinator(DataUpdateCoordinator):
    """Handle individual HTTP fetches from BIND9 metrics endpoint."""

    def __init__(self, hass, host):
        super().__init__(
            hass,
            _LOGGER,
            name=f"BIND9 Stats ({host})",
            update_interval=timedelta(seconds=30),
        )
        self.host = host
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self):
        url = f"http://{self.host}/json/v1/server"
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise UpdateFailed(f"HTTP status error: {response.status}")
                return await response.json()
        except Exception as e:
            raise UpdateFailed(f"Failed communicating with BIND9 server: {e}")
