from ..analytics import AnalyticsView
from ... import dict_admins

# Get the appropriate admin instance
admin = dict_admins["m2_portraits"]

# Add views for each portrait report with unique endpoints
admin.add_view(
    AnalyticsView(
        name="City Portrait",
        endpoint="city_portrait",
        report_name="m2_portraits/CityPortrait.ipynb",
    )
)
admin.add_view(
    AnalyticsView(
        name="Mobility Portrait",
        endpoint="mobility_portrait",
        report_name="m2_portraits/MobilityPortrait.ipynb",
    )
)
admin.add_view(
    AnalyticsView(
        name="GTFS Portrait",
        endpoint="gtfs_portrait",
        report_name="m2_portraits/resmi-Portraits-GTFS.ipynb",
    )
)
