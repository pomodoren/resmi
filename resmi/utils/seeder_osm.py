import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import Tag, CyclingAsset, RoadSegment, AssetType
from app import create_app, db


app = create_app()

data_dicts = [
    {
        "file": "../seeder_data/tirana/cycling.geojson",
        "model": CyclingAsset,
        "asset_type_id": 8,
    },
    {
        "file": "../seeder_data/tirana/roads.geojson",
        "model": RoadSegment,
        "asset_type_id": 2,
    },
]


with app.app_context():
    for item in data_dicts:
        with open(item["file"]) as f:
            data = json.load(f)["features"]

        i = 0
        for each in data:
            i += 1
            if i > 500:
                break
            if "geometry" in each:
                if each["geometry"]["type"] != "LineString":
                    continue
                name = each["type"] + "-" + str(each["id"])
                if "name" in each:
                    name = each["name"]
                if "name" in each["properties"]:
                    name = each["properties"]["name"]
                print(each["id"])

                # Extract geometry coordinates
                geometry_coordinates = [
                    (point[0], point[1]) for point in each["geometry"]["coordinates"]
                ]

                # deal with type
                type = each["type"]
                # type_db = db.session.query(AssetType).filter(name=type).first()
                # if not type_db:

                # Create Asset instance
                model = item["model"]
                asset = model(
                    name=each["type"] + "-" + str(each["id"]),
                    asset_type_id=item["asset_type_id"],
                    osm_id=str(each["id"]),
                    description="",
                    geometry="LINESTRING({})".format(
                        ", ".join(
                            [
                                " ".join(map(str, coord))
                                for coord in geometry_coordinates
                            ]
                        )
                    ),
                )

                # Add tags to the Asset
                if "properties" in each:
                    for key, value in each["properties"].items():
                        tag = Tag(key=key, value=value, asset_id=asset.id)
                        asset.tags.append(tag)

                # Commit changes to the database
                db.session.add(asset)
                db.session.commit()
