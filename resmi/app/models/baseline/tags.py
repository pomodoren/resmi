from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean

from sqlalchemy import event, Text
from sqlalchemy.orm import relationship, validates

from ... import db
from ..mixins import AuditMixinNullable


class Tag(db.Model, AuditMixinNullable):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)

    key = Column(String)
    value = Column(String)
    value_type = Column(String)

    active = Column(Boolean, default=True)
    
    tag_group = Column(String)

    asset_id = Column(Integer, ForeignKey("assets.id"))
    asset = relationship("Asset", back_populates="tags")

    standard_tag_id = Column(Integer, ForeignKey("standard_tags.id"))
    standard_tag = relationship("StandardTag", back_populates="tags")

    def __repr__(self):
        return f"{self.key}: {self.value}"


class StandardTag(db.Model, AuditMixinNullable):
    __tablename__ = "standard_tags"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    description = Column(String)

    asset_type_id = Column(Integer, ForeignKey("asset_types.id"), nullable=False)
    asset_type = relationship("AssetType", back_populates="standard_tags")

    allowed_values = relationship("AllowedTagValue", back_populates="standard_tag")
    tags = relationship("Tag", back_populates="standard_tag")

    def __repr__(self):
        return f"<StandardTag {self.key}>"


class AllowedTagValue(db.Model, AuditMixinNullable):
    __tablename__ = "allowed_tag_values"
    id = Column(Integer, primary_key=True)
    value = Column(String)

    tag_id = Column(Integer, ForeignKey("standard_tags.id"))
    # asset_type = relationship("AssetType", back_populates="standard_tags")

    standard_tag = relationship("StandardTag", back_populates="allowed_values")

    def __repr__(self):
        return f"<{self.value}>"


def validate_and_assign_standard_tag(mapper, connect, target):
    # Access the asset to get the asset type
    if target.asset and target.asset.asset_type:
        # Retrieve all standard tags for the asset's asset type
        standard_tags = target.asset.asset_type.standard_tags

        # Find a standard tag that matches the tag's key
        for st_tag in standard_tags:
            if st_tag.key == target.key:
                target.standard_tag_id = st_tag.id
                break


# Register the listener for both insert and update events
event.listen(Tag, "before_insert", validate_and_assign_standard_tag)
event.listen(Tag, "before_update", validate_and_assign_standard_tag)
