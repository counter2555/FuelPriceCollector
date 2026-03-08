import os
import logging
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from api import SpritpreisAPI, FuelTypes

if __name__ == "__main__":
    # setup logging (use timestamps and log level)
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )

    logging.info("Starting fuel price scraper...")
    logging.info("Address enabled.")
    # get variables
    latitude = float(os.environ.get("LATITUDE", 48.2082))  # Default to Vienna
    longitude = float(os.environ.get("LONGITUDE", 16.3738))  # Default to Vienna
    fuel_type = os.environ.get("FUEL_TYPE", FuelTypes.SUP.value)  # Default to SUP

    # setup prometheus registry and gauge
    logging.info(f"Setting up Prometheus registry and gauge for fuel type: {fuel_type}")
    registry = CollectorRegistry()

    fuel_price_gauge = Gauge(
        "gas_station_fuel_price_euro",
        "Current fuel price at gas station",
        ["station_name", "lat", "long", "fuel_type", "address"],  # Dimensions
        registry=registry,
    )

    # setup api
    api = SpritpreisAPI(
        latitude=latitude,
        longitude=longitude,
        fuel_type=fuel_type,
    )

    logging.info("Fetching gas station data from API...")

    stations = api.fetch_gas_stations()

    # fetch
    for station in stations:
        for price in station.prices or []:
            logging.info(
                f"Processing station: {station.name}, fuel type: {price.fuelType}, price: {price.amount} EUR"
            )
            fuel_price_gauge.labels(
                station_name=station.name,
                lat=station.location.latitude,
                long=station.location.longitude,
                fuel_type=price.fuelType,
                address=station.location.address,
            ).set(price.amount)

    logging.info("Pushing metrics to Prometheus Pushgateway...")
    push_to_gateway(
        os.environ.get("PUSHGATEWAY_URL", "localhost:9091"),
        job="fuel_price_scraper",
        registry=registry,
    )
