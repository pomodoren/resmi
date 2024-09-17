from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Boolean, event

from ... import db
from ..mixins import AuditMixinNullable
from .base import relation_asset_association


class Relation(db.Model, AuditMixinNullable):
    __tablename__ = "relations"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)
    public = Column(Boolean)

    # is it a group to define vid?
    vid_group = Column(Boolean)

    assets = relationship(
        "Asset",
        secondary=relation_asset_association,
        back_populates="relations",
        cascade="all",
    )

    def __repr__(self):
        return f"AG-{self.name}"
