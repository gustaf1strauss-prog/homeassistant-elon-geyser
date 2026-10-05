"""Platform for Elon Geyser sensor integration."""
from __future__ import annotations

from datetime import timedelta
import logging
import requests

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, UnitOfElectricPotential, UnitOfElectricCurrent
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

_LOGGER = logging.getLogger(__name__)

# Polling interval (updates every 30 seconds)
SCAN_INTERVAL = timedelta(seconds=30)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Elon Geyser sensor platform."""
    # Replace this IP with your Elon Geyser IP or retrieve it from config
    geyser_ip = config.get("host", "192.168.7.119")
    
    add_entities([
        ElonGeyserTemperatureSensor(geyser_ip),
        ElonGeyserVoltageSensor(geyser_ip),
        ElonGeyserCurrentSensor(geyser_ip),
    ], True)


class ElonGeyserBaseSensor(SensorEntity):
    """Base class for Elon Geyser sensors."""

    def __init__(self, ip_address: str) -> None:
        """Initialize the sensor."""
        self._ip = ip_address
        self._attr_available = False

    def fetch_data(self) -> dict | None:
        """Fetch json status data from the Elon Geyser unit."""
        try:
            response = requests.get(f"http://{self._ip}/status", timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as err:
            _LOGGER.error("Error communicating with Elon Geyser at %s: %s", self._ip, err)
        return None


class ElonGeyserTemperatureSensor(ElonGeyserBaseSensor):
    """Temperature sensor for Elon Geyser."""

    _attr_name = "Elon Geyser Temperature"
    _attr_unique_id = "elon_geyser_temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data."""
        data = self.fetch_data()
        if data and "temperature" in data:
            self._attr_native_value = data["temperature"]
            self._attr_available = True
        else:
            self._attr_available = False


class ElonGeyserVoltageSensor(ElonGeyserBaseSensor):
    """Voltage sensor for Elon Geyser."""

    _attr_name = "Elon Geyser Voltage"
    _attr_unique_id = "elon_geyser_voltage"
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data."""
        data = self.fetch_data()
        if data and "voltage" in data:
            self._attr_native_value = data["voltage"]
            self._attr_available = True
        else:
            self._attr_available = False


class ElonGeyserCurrentSensor(ElonGeyserBaseSensor):
    """Current sensor for Elon Geyser."""

    _attr_name = "Elon Geyser Current"
    _attr_unique_id = "elon_geyser_current"
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data."""
        data = self.fetch_data()
        if data and "current" in data:
            self._attr_native_value = data["current"]
            self._attr_available = True
        else:
            self._attr_available = False