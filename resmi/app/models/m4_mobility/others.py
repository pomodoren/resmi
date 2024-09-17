from sqlalchemy import Column, Integer, ForeignKey

from ..mixins import GeoMixin
from ..baseline import Asset


class CyclingPath(Asset, GeoMixin):
    __tablename__ = "cycling_paths"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "cycling-path",
    }


class CyclingAsset(Asset, GeoMixin):
    __tablename__ = "cycling_assets"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "cycling-path",
    }


class TaxiStations(Asset, GeoMixin):
    __tablename__ = "taxi_stations"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "taxi-stations",
    }


class ChargingStation(Asset, GeoMixin):
    __tablename__ = "charging_stations"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "charging-stations",
    }


class Sidewalk(Asset, GeoMixin):
    __tablename__ = "sidewalk"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "sidewalk",
    }


class Crossing(Asset, GeoMixin):
    __tablename__ = "crossing"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "crossing",
    }


class Parking(Asset, GeoMixin):
    __tablename__ = "parkings"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "parking",
    }


class RoadAsset(Asset, GeoMixin):
    __tablename__ = "road_assets"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "road-assets",
    }

