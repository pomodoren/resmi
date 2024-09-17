from flask_admin.contrib.geoa import ModelView as MVA
from flask_admin.form import rules


# Create customized model view class
class MyModelView(MVA):

    # scan_delete = False
    page_size = 50
    can_export = True
    # form_excluded_columns = ['id']


class GeoView(MyModelView):
    column_list = ["id", "name", "description", "geometry"]
    # can_edit = False
    # can_create = False
    # can_delete = False


class NonGeoView(MyModelView):
    column_list = ["id", "name", "description"]


class OSMAssetView(GeoView):

    # Define fields to be displayed in the list view
    column_list = ["name", "description", "tags", "geometry"]

    """
    def __init__(self, session, asset_type_filter=None, **kwargs):
        self.asset_type_filter = asset_type_filter
        super(OSMAssetView, self).__init__(models.Asset, session, **kwargs)

    def get_query(self):
        query = super(OSMAssetView, self).get_query()
        if self.asset_type_filter:
            query = query.filter(
                models.Asset.asset_type.has(name=self.asset_type_filter)
            )
        return query

    def get_count_query(self):
        query = super(OSMAssetView, self).get_count_query()
        if self.asset_type_filter:
            query = self.session.query(func.count("*")).filter(
                models.Asset.asset_type.has(name=self.asset_type_filter)
            )
        return query
    """

    # Set the number of items per page in list view
    page_size = 100

    form_rules = (
        (
            (
                rules.HTML(
                    "<div><h3 style='text-align: center;'>On OSM assets</h3></div>"
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
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Description</h3></div><br>"
                ),
                "name",
                "description",
                "osm_id",
            )
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Tags</h3></div><br>"
                ),
                "tags",
            )
        ),
    )
