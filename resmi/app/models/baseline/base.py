from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, Boolean, event

from flask_appbuilder.security.sqla.models import User  # noqa

from datetime import datetime

from ... import db
from ..mixins import AuditMixinNullable
from ..associations import (
    asset_issue_association,
    asset_material_reports_association,
    asset_profile_association,
    asset_event_association,
)
from .tags import Tag

relation_asset_association = Table(
    "relation_asset_association",
    db.Model.metadata,
    Column("relation_id", Integer, ForeignKey("relations.id")),
    Column("asset_id", Integer, ForeignKey("assets.id")),
)



class Asset(db.Model, AuditMixinNullable):
    __tablename__ = "assets"

    # ids
    id = Column(Integer, primary_key=True)

    # type_sequential_id = Column(Integer) # seq id for vid
    vid = Column(String, unique=True)  # visual ID, useful for priting
    vid_version = Column(String)
    osm_id = Column(String)

    # desc
    name = Column(String)
    description = Column(String)

    public = Column(Boolean)
    active = Column(Boolean, default=True)

    parent_asset_id = Column(Integer, ForeignKey("assets.id"))
    tags = relationship("Tag", back_populates="asset")

    type = Column(String)

    asset_type_id = Column(Integer, ForeignKey("asset_types.id"), nullable=False)
    asset_type = relationship("AssetType", back_populates="assets")

    relations = relationship(
        "Relation", secondary=relation_asset_association, back_populates="assets"
    )

    issues = relationship(
        "Issue", secondary=asset_issue_association, back_populates="affected_assets"
    )
    events = relationship(
        "Event", secondary=asset_event_association, back_populates="affected_assets"
    )
    material_reports = relationship(
        "MaterialReport",
        secondary=asset_material_reports_association,
        back_populates="affected_assets",
    )

    lifecycle_profiles = relationship(
        "LifecycleProfile", secondary=asset_profile_association, back_populates="assets"
    )

    # Relationship to access all images associated with this asset
    images = db.relationship(
        "Image", back_populates="asset", cascade="all, delete-orphan"
    )

    # Polymorphic configuration
    __mapper_args__ = {"polymorphic_identity": "asset", "polymorphic_on": type}

    def generate_vid(self):
        if self.asset_type.name == "bus-stop":
            if self.type == "asset":
                self.vid = f"s{self.name}-a{self.asset_type.name}{self.id:04}-v{datetime.utcnow().strftime('%Y%m')}"
            else:
                self.vid = f"s{self.name}"
        elif self.asset_type.name == "bus":
            self.vid = f"b{self.name}"
        elif self.asset_type.name == "bus type":
            self.vid = f"b{self.name}-a{self.asset_type.name}{self.id:04}-v{datetime.utcnow().strftime('%Y%m')}"
        else:
            self.vid = f"Asset-{self.id}"

    def __repr__(self):
        return f"Asset-{self.id}"


class AssetType(db.Model, AuditMixinNullable):
    __tablename__ = "asset_types"
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)
    version = Column(String)
    producer = Column(String)

    asset_type_group = Column(String)

    # vid
    # c01-s11012-a2103-v2406
    #   - city-station_area_no-asset_type_asset_no-version_date
    # c01-b11A001-a3201-v2406
    #   - city-bus_line_bus_no-asset_type_asset_no-version_date
    vid_inherit_city_id = Column(Boolean)
    vid_inherit_parent_id = Column(Boolean)
    vid_inherit_group_id = Column(Boolean)
    vid_inherit_type = Column(Boolean)
    vid_inherit_version = Column(Boolean)

    description = Column(Text)
    assets = relationship("Asset", back_populates="asset_type")
    standard_tags = relationship("StandardTag", back_populates="asset_type")

    def __repr__(self):
        return f"AT-{self.name}"


def asset_insert_listener(mapper, connection, target):
    # Create a session factory that is bound to the connection
    session_factory = sessionmaker(bind=connection)
    # Create a scoped session
    session = scoped_session(session_factory)

    # CREATE STANDARD TAGS
    # target is the newly created Asset instance
    if target.asset_type and target.asset_type.standard_tags:
        # Loop through each standard tag associated with the asset type
        for standard_tag in target.asset_type.standard_tags:
            # Create a new Tag with an empty value
            new_tag = Tag(
                asset_id=target.id,
                key=standard_tag.key,
                value=None,  # Set an empty string or a default value
                value_type="default_type",  # Modify as needed
                active=True,
                standard_tag_id=standard_tag.id,
            )
            # Add the new Tag to the session (this assumes you're using a session-based approach)
            session.add(new_tag)
        # Commit changes if necessary, handle with care
        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise

    # GENERATE VID
    target.generate_vid()
    connection.execute(
        Asset.__table__.update().where(Asset.id == target.id).values(vid=target.vid)
    )


event.listen(Asset, "after_insert", asset_insert_listener)
