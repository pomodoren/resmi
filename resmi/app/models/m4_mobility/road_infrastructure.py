from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, Boolean

from ..mixins import GeoMixin
from ..baseline import Asset
from ..options import (
    MaterialType,
    VisibilityLevel,
    Status,
    Accessibility,
    SurfaceType,
    TrafficFlow,
)


class Road(Asset):
    __tablename__ = "roads"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "road",
    }


class RoadSegment(Asset, GeoMixin):
    __tablename__ = "road_segments"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "road_segment",
    }


class TrafficSignal(Asset, GeoMixin):
    __tablename__ = "traffic_signals"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "road_asset",
    }
