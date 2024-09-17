from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Enum,
    Float,
    Boolean,
)

from ... import db
from ..options import DepreciationType, CostUnitType
from ..mixins import AuditMixinNullable


class CostType(db.Model, AuditMixinNullable):
    __tablename__ = "cost_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Text)

    def __repr__(self):
        return f"{self.name}"


class Cost(db.Model, AuditMixinNullable):
    __tablename__ = "costs"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    version = Column(String)
    description = Column(Text)

    cost_type_id = Column(Integer, ForeignKey("cost_types.id"))
    cost_type = relationship("CostType")

    asset_type_id = Column(Integer, ForeignKey("asset_types.id"))
    asset_type = relationship("AssetType")

    activity_type_id = Column(Integer, ForeignKey("lifecycle_activity_types.id"))
    activity_type = relationship("LifecycleActivityType")

    cost_money = Column(Float, nullable=False)
    cost_unit_type = Column(Enum(CostUnitType))

    cost_employee_hours = Column(Float, nullable=False)

    include = Column(Boolean)
    includes_children = Column(Boolean)
    active = Column(Boolean, default=True)

    depreciation_type = Column(Enum(DepreciationType))

    def __repr__(self):
        return f"{self.name}"
