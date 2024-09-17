import json
import os
from app import db
from app.models import Tag, CyclingAsset, RoadSegment
from .importers_base import BaseImporterView


class OSMImporterView(BaseImporterView):
    """
    OSM specific file importer that inherits from BaseImporterView.
    """
    template = "admin/upload_template_4.html"  # Default template

    def get_file_extension(self):
        return ".geojson"

    def get_processing_function(self):
        return self.process_osm_file

    def process_osm_file(self, file_path):
        """
        Process the uploaded OSM JSON file and import the data to the database.
        """
        data_dicts = [
            {"file": file_path, "model": CyclingAsset, "asset_type_id": 8},
            {"file": file_path, "model": RoadSegment, "asset_type_id": 2},
        ]

        for item in data_dicts:
            with open(item["file"]) as f:
                data = json.load(f)["features"]

            i = 0
            for each in data:
                i += 1
                if i > 500:
                    break
                if "geometry" in each and each["geometry"]["type"] == "LineString":
                    name = each["type"] + "-" + str(each["id"])
                    if "name" in each:
                        name = each["name"]
                    if "name" in each["properties"]:
                        name = each["properties"]["name"]
                    print(f"Processing OSM ID: {each['id']}")

                    # Extract geometry coordinates
                    geometry_coordinates = [
                        (point[0], point[1])
                        for point in each["geometry"]["coordinates"]
                    ]

                    # Create Asset instance
                    model = item["model"]
                    asset = model(
                        name=name,
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

                    db.session.add(asset)
                    db.session.commit()

        os.remove(file_path)
