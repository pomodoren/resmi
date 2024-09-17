from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
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

# from sqlalchemy.ext.declarative import declarative_base
from ... import db  # Assuming you have already defined db
from ..options import ConditionCheck
from ..associations import asset_material_reports_association


class MaterialReport(db.Model):
    __tablename__ = "material_reports"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    timestamp = Column(DateTime, default=func.now())

    # Relationships
    conditions = relationship("Condition", back_populates="material_report")
    affected_assets = relationship(
        "Asset",
        secondary=asset_material_reports_association,
        back_populates="material_reports",
    )
    activity_id = Column(Integer, ForeignKey("lifecycle_activities.id"))
    activity = relationship("LifecycleActivity", back_populates="reports")
    conditions = relationship("Condition", back_populates="report")


class Condition(db.Model):
    __tablename__ = "conditions"
    id = Column(Integer, primary_key=True)

    response = Column(String)
    status = Column(Enum(ConditionCheck, name="status"))
    notes = Column(Text)

    timestamp = Column(DateTime, default=func.now())

    # Relationships
    condition_type = relationship("ConditionType", back_populates="conditions")
    condition_type_id = Column(Integer, ForeignKey("condition_types.id"))

    report_id = Column(Integer, ForeignKey("material_reports.id"))
    report = relationship("MaterialReport", back_populates="conditions")

    def __repr__(self):
        return f"{self.name}"


class ConditionType(db.Model):
    __tablename__ = "condition_types"
    id = Column(Integer, primary_key=True)

    # functions = relationship("Function", back_populates="rule")
    # attributes = relationship("Attribute", back_populates="rule")
    function = Column(String)
    attribute = Column(String)
    operator = Column(String)  # You may want to define an Enum for operators
    value = Column(Float)
    unit = Column(String)
    conditions = relationship("Condition", back_populates="condition_type")

    def __repr__(self):
        return (
            f"{self.function}({self.attribute}){self.operator}{self.value}{self.unit}"
        )


class Function(db.Model):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True)
    # rule_id = Column(Integer, ForeignKey('rules.id'))
    name = Column(String)

    # rule = relationship("Rule", back_populates="functions")


class Attribute(db.Model):
    __tablename__ = "attributes"
    id = Column(Integer, primary_key=True)
    # rule_id = Column(Integer, ForeignKey('rules.id'))
    name = Column(String)

    # rule = relationship("Rule", back_populates="attributes")
