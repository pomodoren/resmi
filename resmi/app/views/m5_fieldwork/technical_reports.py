from flask_admin.form import rules
from ..default_view import GeoView, NonGeoView


class MaterialReportsView(GeoView):
    # Define fields to be displayed in the list view
    column_list = ["name", "timestamp", "type", "description"]

    # Set the number of items per page in list view
    page_size = 50

    form_rules = (
        (
            (rules.HTML("<div><h3 style='text-align: center;'>On Reports</h3></div>"),),
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Description</h3></div><br>"
                ),
                "name",
                "type",
                "description",
                "timestamp",
            ),
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Rules</h3></div><br>"
                ),
                "rules",
            )
        ),
    )


class RuleView(NonGeoView):
    column_list = ["id", "function", "attribute", "operator", "value"]
