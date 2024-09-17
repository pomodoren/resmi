from flask_admin.form import rules
from wtforms.fields import StringField
from ..default_view import GeoView, NonGeoView


class LifecycleProfileView(GeoView):
    # Define fields to be displayed in the list view
    column_list = ["name", "assigned_to", "activities"]

    # Set the number of items per page in list view
    page_size = 50

    form_rules = (
        (
            (
                rules.HTML("<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Lifecycle profile</h3></div><br>"),
                "name",
                "description",
                "assigned_to"
            )
        ),
        (
            (
                rules.HTML("<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Activities for assets</h3></div><br>"),
                "activities",
                "assets"
            )
        ),
    )


class LifecycleActivityView(GeoView):
    # Define fields to be displayed in the list view
    column_list = [ "name", "status", "recursive", "description", "activity_type", "start_date", "assigned_to"]

    # Set the number of items per page in list view
    page_size = 50

    form_rules = (
        (
            (
                rules.HTML("<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Lifecycle activity</h3></div><br>"),
                "name",
                "description",
                "recursive",
                "status"
            )
        ),
        (
            (
                rules.HTML("<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Additional information?</h3></div><br>"),
                "assigned_to",
                "activity_type",
                "profiles",
            )
        ),
    )


class LifecycleActivityTypeView(GeoView):
    # Define fields to be displayed in the list view
    column_list = ["name", "description", "assigned_to"]

    # Set the number of items per page in list view
    page_size = 50

    form_rules = (
        (
            (
                rules.HTML("<div style='background-color: #e3ffd7; border-top: 3px solid lightgrey;'><h3 style='text-align: center;'>Lifecycle activity type</h3></div><br>"),
                "name",
                "description",
            )
        ),
    )

