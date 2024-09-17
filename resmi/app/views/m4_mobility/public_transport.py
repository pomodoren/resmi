from flask_admin.form import rules
from ..default_view import GeoView


class BusStopView(GeoView):

    # Define fields to be displayed in the list view
    column_list = ["stop_id", "stop_name", "stop_desc", "geometry", "children"]

    # Set the number of items per page in list view
    page_size = 100

    form_rules = (
        (
            (
                rules.HTML(
                    "<div><h3 style='text-align: center;'>On bus stops</h3></div>"
                ),
            ),
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Geo Info</h3></div><br>"
                ),
                "geometry",
            ),
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>GTFS Info</h3></div><br>"
                ),
                "stop_id",
                "stop_code",
                "stop_name",
                "stop_desc",
                "wheelchair_boarding",
            )
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Infrastructure</h3></div><br>"
                ),
                "asphalt_quality",
                "pavement_quality",
                "pavement_width",
                "sidewalk_curb_height",
                "road_type_section",
                "engineering_network",
            )
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Safety</h3></div><br>"
                ),
                "street_segment_description",
                "distance_from_nearest_intersection",
                "vertical_signage",
                "horizontal_signage",
                "minimum_curb_cab_clearance",
                "seat_from_curb_distance",
                "greening",
            )
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #ffdcf1; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>GTFS Extra</h3></div><br>"
                ),
                "zone_id",
                "stop_url",
                "location_type",
                "stop_timezone",
                "level_id",
                "platform_code",
            )
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>OpenStreetMap Tags</h3></div><br>"
                ),
                "tags",
            )
        ),
    )
