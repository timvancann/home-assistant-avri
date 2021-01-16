"""The avri component."""
import asyncio
from datetime import timedelta

from avri.api import Avri

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_HOUSE_NUMBER, CONF_ZIP_CODE, DOMAIN

PLATFORMS = ["sensor"]
SCAN_INTERVAL = timedelta(hours=4)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Avri component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Avri from a config entry."""
    client = Avri(
        postal_code=entry.data[CONF_ZIP_CODE],
        house_nr=entry.data[CONF_HOUSE_NUMBER],
    )

    hass.data[DOMAIN][entry.entry_id] = client

    for component in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
                for component in PLATFORMS
            ]
        )
    )
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
