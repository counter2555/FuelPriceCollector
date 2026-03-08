import requests
import logging
from enum import Enum
from models import GasStationPublic


class FuelTypes(Enum):
    SUP = "SUP"
    DIE = "DIE"


class SpritpreisAPI:
    def __init__(
        self,
        latitude: float,
        longitude: float,
        fuel_type: str,
        include_closed: bool = True,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.fuel_type = fuel_type
        self.include_closed = include_closed

    def fetch_gas_stations(self) -> list[GasStationPublic]:
        url = f"https://api.e-control.at/sprit/1.0/search/gas-stations/by-address?latitude={self.latitude}&longitude={self.longitude}&fuelType={self.fuel_type}&includeClosed={str(self.include_closed).lower()}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        stations = [GasStationPublic(**x) for x in response.json()]
        logging.info(f"Fetched {len(stations)} gas stations from API.")
        return stations
