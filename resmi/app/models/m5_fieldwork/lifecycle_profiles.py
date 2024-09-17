from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Enum,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ... import db
from ..associations import asset_profile_association
from ..mixins import AuditMixinNullable, AssignableMixin
from ..options import ActivityStatus


lifecycle_profile_activity_association = Table(
    "lifecycle_profile_activity_association",
    db.Model.metadata,
    Column("profile_id", Integer, ForeignKey("lifecycle_profiles.id")),
    Column("activity_id", Integer, ForeignKey("lifecycle_activities.id")),
)


class LifecycleProfile(db.Model, AuditMixinNullable, AssignableMixin):
    __tablename__ = "lifecycle_profiles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)

    activities = relationship(
        "LifecycleActivity",
        secondary=lifecycle_profile_activity_association,
        back_populates="profiles",
    )

    assigned_to_id = Column(Integer, ForeignKey("ab_user.id"), nullable=True)
    assigned_to = relationship("User", uselist=False, foreign_keys=[assigned_to_id])

    notes = Column(Text)

    assets = relationship(
        "Asset",
        secondary=asset_profile_association,
        back_populates="lifecycle_profiles",
    )

    def __repr__(self):
        return f"{self.name}"


class LifecycleActivity(db.Model, AuditMixinNullable):
    __tablename__ = "lifecycle_activities"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    description = Column(Text)
    recursive = Column(Boolean, default=False)

    assigned_to_id = Column(Integer, ForeignKey("ab_user.id"), nullable=True)
    assigned_to = relationship("User", uselist=False, foreign_keys=[assigned_to_id])

    activity_type_id = Column(Integer, ForeignKey("lifecycle_activity_types.id"))
    activity_type = relationship("LifecycleActivityType")

    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, default=func.now())

    status = Column(Enum(ActivityStatus, name="status"))
    notes = Column(Text)

    reports = relationship("MaterialReport", back_populates="activity")
    files = db.relationship("File", back_populates="activity", cascade="all, delete-orphan")

    profiles = relationship(
        "LifecycleProfile",
        secondary=lifecycle_profile_activity_association,
        back_populates="activities",
    )

    @property
    def starting_date(self):
        return self.start_date.strftime("%Y-%m-%d") if self.start_date else None

    @property
    def ending_date(self):
        return self.end_date.strftime("%Y-%m-%d") if self.end_date else None

    def __repr__(self):
        return f"{self.name}"


class LifecycleActivityType(db.Model, AuditMixinNullable):
    __tablename__ = "lifecycle_activity_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)

    def __repr__(self):
        return f"{self.name}"
