"""
The "esphome_fake_dlbm" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the esphome_fake_dlbm component you will need to add the following to your
configuration.yaml file.

esphome_fake_dlbm:
"""
from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "esphome_fake_dlbm"


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up a skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.set('esphome_fake_dlbm.Hello_World', 'Works!')

    # Return boolean to indicate that initialization was successfully.
    return True