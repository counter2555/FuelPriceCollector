import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import (
    Integer,
    create_engine,
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, Mapped, Session, relationship

Base = declarative_base()


class FuelPriceEntry(Base):
    __tablename__ = "fuel_price_entries"
    id: Mapped[int] = Column(Integer, primary_key=True)
    station: Mapped["FuelStation"] = relationship(
        "FuelStation", back_populates="prices"
    )
    station_id: Mapped[int] = Column(
        Integer, ForeignKey("fuel_stations.id"), nullable=False
    )
    fuel_type: Mapped[str] = Column(String, nullable=False)
    price: Mapped[float] = Column(Float, nullable=False)
    timestamp: Mapped[datetime] = Column(
        DateTime, default=datetime.now(tz=timezone.utc)
    )


class FuelStation(Base):
    __tablename__ = "fuel_stations"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String, nullable=False)
    latitude: Mapped[float] = Column(Float, nullable=False)
    longitude: Mapped[float] = Column(Float, nullable=False)
    city: Mapped[str] = Column(String, nullable=True)
    address: Mapped[str] = Column(String, nullable=True)
    postal_code: Mapped[str] = Column(String, nullable=True)

    prices = relationship("FuelPriceEntry", back_populates="station")


class DBHandler:
    def __init__(self, db_url: str):
        self.engine = create_engine(f"sqlite:///{db_url}")
        Base.metadata.create_all(self.engine)

    def add_entries(self, entries: FuelPriceEntry | list[FuelPriceEntry]):
        with Session(self.engine) as session:
            if not isinstance(entries, list):
                entries = [entries]
            for entry in entries:
                existing_station = (
                    session.query(FuelStation).filter_by(id=entry.station.id).first()
                )

                if existing_station:
                    entry.station = existing_station
                session.add(entry)
            session.commit()

    def add_station(self, station: FuelStation):
        """adds the fuel station to the database if no station with the same id exists

        Args:
            station (FuelStation): Fuel Station
        """
        with Session(self.engine) as session:
            to_add: list[FuelStation] = []
            existing_station = (
                session.query(FuelStation).filter_by(id=station.id).first()
            )
            if not existing_station:
                to_add.append(station)

            if len(to_add) > 0:
                session.add_all(to_add)
                session.commit()

    def get_prices(self) -> pd.DataFrame:
        """returns a dataframe that contains all price points, the station name and address

        Returns:
            pd.DataFrame: dataframe with columns station_id, station_name, station_address, fuel_type, price, timestamp
        """
        with Session(self.engine) as session:
            query = (
                session.query(
                    FuelPriceEntry.station_id,
                    FuelStation.name.label("station_name"),
                    FuelStation.address.label("station_address"),
                    FuelPriceEntry.fuel_type,
                    FuelPriceEntry.price,
                    FuelPriceEntry.timestamp,
                )
                .join(FuelStation, FuelPriceEntry.station_id == FuelStation.id)
                .order_by(FuelPriceEntry.timestamp.desc())
            )
            df = pd.DataFrame(
                query.all(),
                columns=[
                    "station_id",
                    "station_name",
                    "station_address",
                    "fuel_type",
                    "price",
                    "timestamp",
                ],
            )
            return df.sort_values(by="timestamp", ascending=False)