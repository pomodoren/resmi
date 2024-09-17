from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ... import db
from ..associations import asset_issue_association
from ..mixins import GeoMixin


class Issue(db.Model, GeoMixin):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=func.now(), nullable=False)

    severity = Column(String)
    category = Column(
        Enum(
            "safety",
            "infrastructure",
            "pedestrians",
            "cycling",
            name="category of issue",
        ),
        default="infrastructure",
    )
    #status = Column(
    #    Enum(
    #        "received", "accepted", "in-process", "solved", "postponed", name="status"
    #    ),
    #    default="received",
    #)
    issuer = Column(String)

    # Relationship with Asset
    affected_assets = relationship(
        "Asset", secondary=asset_issue_association, back_populates="issues"
    )

    def __repr__(self):
        return f"I-{self.name}"

