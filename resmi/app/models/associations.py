from sqlalchemy import Column, Integer, ForeignKey, Table
from .. import db



# Association table between assets and issues
asset_material_reports_association = Table(
    "asset_material_reports_association",
    db.Model.metadata,
    Column("material_reports_id", Integer, ForeignKey("material_reports.id")),
    Column("asset_id", Integer, ForeignKey("assets.id")),
)


asset_profile_association = Table(
    "asset_profile_association",
    db.Model.metadata,
    Column("asset_id", Integer, ForeignKey("assets.id")),
    Column("profile_id", Integer, ForeignKey("lifecycle_profiles.id")),
)


# Association table between assets and issues
asset_issue_association = Table(
    "asset_issue_association",
    db.Model.metadata,
    Column("asset_id", Integer, ForeignKey("assets.id")),
    Column("issue_id", Integer, ForeignKey("issues.id")),
)

# Association table between events and assets
asset_event_association = Table(
    "asset_event_association",
    db.Model.metadata,
    Column("event_id", Integer, ForeignKey("events.id")),
    Column("asset_id", Integer, ForeignKey("assets.id")),
)
