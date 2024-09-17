from flask_admin.form import rules
from ..default_view import GeoView


class IssueView(GeoView):

    # Define fields to be displayed in the list view
    column_list = [
        "name",
        "category",
        "timestamp",
        "category",
        "description",
    ]

    # Set the number of items per page in list view
    page_size = 50

    form_rules = (
        (
            (rules.HTML("<div><h3 style='text-align: center;'>On Issues</h3></div>"),),
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Geo Info</h3></div><br>"
                ),
                "geometry",
            ),
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Description</h3></div><br>"
                ),
                "name",
                "description",
                "timestamp",
                "severity",
                "category",
            ),
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Status</h3></div><br>"
                ),
                # "status",
                "response",
                "issuer",
            )
        ),
        (
            (
                rules.HTML(
                    "<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Affected Assets</h3></div><br>"
                ),
                "affected_assets",
            )
        ),
    )
