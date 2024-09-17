import requests
from sqlalchemy import Column
from geoalchemy2 import Geometry

from datetime import datetime, timezone
from flask_appbuilder.models.mixins import AuditMixin

from flask import g
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr

import sqlalchemy as sa
from .. import db

import pytz

utc = pytz.UTC


class GeoMixin(object):
    geometry = Column(Geometry(geometry_type="GEOMETRY", srid=4326))

    # TODO: develop stats for this kind of file


class OSMMixin(object):
    # TODO: map OSM stuff to ASSET_TYPE_DICT

    @classmethod
    def fetch_osm_data(cls, query):
        url = "http://overpass-api.de/api/interpreter"
        response = requests.get(url, params={"data": query})
        return response.json()

    @classmethod
    def import_osm_assets(cls, session, query, asset_type, parent_id=None):

        # Fetch data
        data = cls.fetch_osm_data(query)

        # Import data into the database
        for element in data["elements"]:
            # Assuming 'name' can be extracted (this might not be the case for all asset types)
            name = element.get("tags", {}).get("name", "Unnamed")
            asset = cls(name=name, asset_type=asset_type, parent_id=parent_id)
            session.add(asset)

        session.commit()


class DBMixin(object):

    def save(self, session):
        session.add(self)
        session.flush()
        return self

    def delete(self, session):
        session.delete(self)
        session.flush()


class AuditMixinNullable(AuditMixin):

    created_on = sa.Column(
        db.Date,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None).date(),
        nullable=True,
    )
    changed_on = sa.Column(
        db.Date,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None).date(),
        onupdate=lambda: datetime.now(timezone.utc).replace(tzinfo=None).date(),
        nullable=True,
    )

    @declared_attr
    def created_by_fk(cls):
        return Column(
            Integer, ForeignKey("ab_user.id"), default=cls.get_user_id, nullable=True
        )

    @declared_attr
    def changed_by_fk(cls):
        return Column(
            Integer,
            ForeignKey("ab_user.id"),
            default=cls.get_user_id,
            onupdate=cls.get_user_id,
            nullable=True,
        )


class AssignableMixin(object):

    @declared_attr
    def assigned_to(cls):
        return Column(
            Integer, ForeignKey("ab_user.id"), default=cls.get_user_id, nullable=True
        )
