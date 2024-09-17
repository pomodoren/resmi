from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Enum,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ... import db
from ..mixins import GeoMixin, AuditMixinNullable
from ..associations import asset_event_association


class Event(db.Model, GeoMixin, AuditMixinNullable):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    type = Column(Enum("hazard_event", name="event_type"), default="hazard_event")
    return_per = Column(Float)
    intensity = Column(Float)
    affected_assets = relationship(
        "Asset", secondary=asset_event_association, back_populates="events"
    )
    timestamp = Column(DateTime, default=func.now(), nullable=False)

    __mapper_args__ = {"polymorphic_identity": "event", "polymorphic_on": type}


class HazardEvent(Event):
    __tablename__ = "hazard_reports"
    id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    # Add any additional fields specific to HazardEvent here
    # Example: hazard_type = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": "hazard_event",
    }
