from .assets import AssetView, AssetTypeView
from ..analytics import AnalyticsView
from ... import dict_admins, db, models

admin = dict_admins["m3_assets"]

stats_view = AnalyticsView(
    name="My Assets",
    endpoint="m3_assets",
    url="/m3_assets",
    report_name="m3_assets/resmi-Assets.ipynb",
)

# Set the AnalyticsView as the index view
#admin._set_admin_index_view(stats_view)
# admin.static_url_path = '/static'

admin.add_view(
    AssetView(
        models.Asset, db.session, name="Assets"
    )
)

admin.add_view(
    AssetTypeView(
        models.AssetType, db.session, name="Asset Types"
    )
)
