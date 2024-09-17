import pandas as pd

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Float, Enum, Boolean, Text
from sqlalchemy.orm import Session

from ..mixins import GeoMixin
from ..baseline import Asset
from ..options import StandardQuality, StandardPresence


class BusStop(Asset, GeoMixin):
    __tablename__ = "bus_stops"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)

    # gtfs stuff
    stop_id = Column(Integer)
    stop_code = Column(String)
    stop_name = Column(String)
    stop_desc = Column(Text)
    zone_id = Column(Integer)
    stop_url = Column(String)
    location_type = Column(Integer)
    stop_timezone = Column(Integer)
    wheelchair_boarding = Column(Integer)
    level_id = Column(Integer)
    platform_code = Column(Integer)

    # infra stuff
    asphalt_quality = Column(Enum(StandardQuality))
    pavement_quality = Column(Enum(StandardQuality))
    pavement_width = Column(Float)
    sidewalk_curb_height = Column(Float)
    road_type_section = Column(String)
    engineering_network = Column(Enum(StandardPresence))

    # safety stuff
    street_segment_description = Column(String)
    distance_from_nearest_intersection = Column(Float)

    vertical_signage = Column(Enum(StandardPresence))
    horizontal_signage = Column(Enum(StandardPresence))

    minimum_curb_cab_clearance = Column(String)
    seat_from_curb_distance = Column(String)
    greening = Column(Enum(StandardPresence))

    nearest_intersection_id = Column(Integer)

    # Polymorphic configuration
    __mapper_args__ = {
        "polymorphic_identity": "bus_stop",
    }

    def get_lat_lon(self):
        """From geometry field extract lat lon for GTFS."""
        # Assuming geometry is stored as a well-known text (WKT) point
        if self.geometry:
            return self.geometry.x, self.geometry.y
        return None, None

    def get_parent_station(self):
        """From parent of asset, get parent_station necessary for GTFS."""
        return self.parent

    @classmethod
    def import_from_gtfs(cls, df):
        """Import bus stop data from a pandas DataFrame."""
        stops = []
        for _, row in df.iterrows():
            stop = cls(
                stop_id=row["stop_id"],
                stop_code=row["stop_code"],
                stop_name=row["stop_name"],
                stop_desc=row["stop_desc"],
                zone_id=row["zone_id"],
                stop_url=row["stop_url"],
                location_type=row["location_type"],
                stop_timezone=row["stop_timezone"],
                wheelchair_boarding=row["wheelchair_boarding"],
                level_id=row["level_id"],
                platform_code=row["platform_code"],
                # Convert latitude and longitude into a geometry object
                geometry="POINT({} {})".format(row["stop_lon"], row["stop_lat"]),
                asset_type_id=1,
                public=True,
                name=row["stop_name"],
                description=row["stop_desc"],
            )
            stops.append(stop)
        # Add logic to commit to the database if using a session
        return stops

    @classmethod
    def export_to_gtfs(cls, session: Session, filepath: str):
        """Export bus stop data to a GTFS-compatible CSV file."""
        # Querying the database for all bus stops
        bus_stops = session.query(BusStop).all()

        # Prepare data for DataFrame
        data = []
        for stop in bus_stops:
            stop_lat, stop_lon = stop.get_lat_lon()
            data.append(
                {
                    "stop_id": stop.stop_id,
                    "stop_code": stop.stop_code,
                    "stop_name": stop.stop_name,
                    "stop_desc": stop.stop_desc,
                    "stop_lat": stop_lat,
                    "stop_lon": stop_lon,
                    "zone_id": stop.zone_id,
                    "stop_url": stop.stop_url,
                    "location_type": stop.location_type,
                    "parent_station": stop.get_parent_station(),
                    "stop_timezone": stop.stop_timezone,
                    "wheelchair_boarding": stop.wheelchair_boarding,
                    "level_id": stop.level_id,
                    "platform_code": stop.platform_code,
                }
            )

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Handling missing data by replacing NaN with empty strings or appropriate defaults
        df.fillna("", inplace=True)

        return df


class Bench(Asset, GeoMixin):
    __tablename__ = "benches"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    # Assuming benches have a material attribute as an example
    material = Column(String)
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)


class Bin(Asset, GeoMixin):
    __tablename__ = "bins"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    # Assuming bins might have a capacity attribute
    capacity = Column(Integer)
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)


class TimetableInfo(Asset, GeoMixin):
    __tablename__ = "timetable_infos"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    # For simplicity, using String; could be detailed with specific Enum or related fields
    departure_board_type = Column(String)
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)


class Advertisement(Asset, GeoMixin):
    __tablename__ = "advertisements"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    # Enum for type of advertisement could be added here
    ad_type = Column(String)
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)


class BusStopSign(Asset, GeoMixin):
    __tablename__ = "bus_stop_signs"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    # Assuming bus stop signs might have an attribute for visibility
    visibility = Column(String)
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)


"""
# Example for another asset, e.g., Cabin
class Cabin(Asset):
    __tablename__ = "cabins"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    cabin_category = Column(String)  # Example, could also be an Enum
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)



class TactilePaving(Asset):
    __tablename__ = "tactile_pavings"

    id = Column(Integer, ForeignKey("assets.id"), primary_key=True)
    # Enum for presence of tactile paving; for simplicity, using Boolean
    is_present = Column(Boolean)
    parent_id = Column(Integer, ForeignKey("bus_stops.id"), nullable=False)
"""
