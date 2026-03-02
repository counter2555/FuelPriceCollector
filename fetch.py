import os
from api import SpritpreisAPI, FuelTypes
from db import DBHandler, FuelPriceEntry, FuelStation

def fetch_and_store_fuel_prices(database_path: str, latitude: float, longitude: float, fuel_type: FuelTypes):
    api = SpritpreisAPI(
        latitude=latitude,
        longitude=longitude,
        fuel_type=fuel_type,
    )
    stations = api.fetch_gas_stations()

    db_handler = DBHandler(db_url=database_path)

    for station in stations:
        fuel_station = FuelStation(
            id=station.id,
            name=station.name,
            latitude=station.location.latitude,
            longitude=station.location.longitude,
            city=station.location.city,
            address=station.location.address,
            postal_code=station.location.postalCode,
        )

        for price in station.prices or []:
            price_entry = FuelPriceEntry(
                station=fuel_station, fuel_type=price.fuelType, price=price.amount
            )
            db_handler.add_entries(price_entry)

def main():
    if "latitude" in os.environ:
        latitude = float(os.environ["latitude"])
    else:
        latitude = 48.2082  # Default to Vienna
    if "longitude" in os.environ:
        longitude = float(os.environ["longitude"])
    else:
        longitude = 16.3738  # Default to Vienna

    if "database_path" in os.environ:
        database_path = os.environ["database_path"]
    else:
        database_path = "./fuel_prices.db"

    fetch_and_store_fuel_prices(database_path=database_path, latitude=latitude, longitude=longitude, fuel_type=FuelTypes.SUP)