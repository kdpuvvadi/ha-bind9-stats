import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "bind9_stats"


class BIND9StatsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for BIND9 Statistics."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}

        if user_input is not None:
            host = (
                user_input["host"]
                .strip()
                .replace("http://", "")
                .replace("https://", "")
            )
            user_input["host"] = host

            # Validate connection before saving
            session = async_get_clientsession(self.hass)
            try:
                url = f"http://{host}/json/v1/server"
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        # Prevent configuring duplicate hosts
                        await self.async_set_unique_id(host)
                        self._abort_if_unique_id_configured()

                        return self.async_create_entry(
                            title=f"BIND9 ({host})", data=user_input
                        )
                    errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host", default="10.10.10.10:8080"): str,
                }
            ),
            errors=errors,
        )
