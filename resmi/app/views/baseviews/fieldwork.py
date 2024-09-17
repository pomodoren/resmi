from flask_appbuilder import ModelView, MasterDetailView, MultipleView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from .notebooks import convert_notebook_to_html
from ...models import (
    LifecycleProfile,
    LifecycleActivity,
    LifecycleActivityType,
    Cost,
    CostType,
)


class CostView(ModelView):
    datamodel = SQLAInterface(Cost)
    list_columns = [
        "name",
        "version",
        "active",
        "asset_type",
        "activity_type",
        "cost_type.depreciation_type",
    ]
    show_fieldsets = [
        ("Main Info", {"fields": ["name", "description", "version", "active"]}),
        ("Related to", {"fields": ["asset_type", "activity_type"]}),
        (
            "Costs",
            {
                "fields": [
                    "cost_type",
                    "cost_money",
                    "cost_unit_type",
                    "cost_employee_hours",
                    "depreciation_type",
                    "include",
                    "includes_children",
                ]
            },
        ),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class CostTypeView(ModelView):
    datamodel = SQLAInterface(CostType)
    list_columns = ["name", "description"]

    show_fieldsets = [
        ("Main Info", {"fields": ["name", "description"]}),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class CostMasterView(MasterDetailView):
    datamodel = SQLAInterface(CostType)
    list_columns = ["name"]  # , "description"] # , "assigned_to", "activities"]
    page_size = 50

    related_views = [CostView]


class ActivityTypesView(ModelView):
    datamodel = SQLAInterface(LifecycleActivityType)
    list_columns = ["name", "description"]

    # related_views = [ContactModelView]
    show_fieldsets = [
        (
            "Main Info",
            {
                "fields": [
                    "name",
                    "description",
                ]
            },
        ),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class ActivityView(ModelView):
    datamodel = SQLAInterface(LifecycleActivity)
    list_columns = [
        "id",
        "name",
        "status",
        "starting_date",
        "ending_date",
        "assigned_to",
    ]
    page_size = 50

    # related_views = [ContactModelView]
    show_fieldsets = [
        ("Main Info", {"fields": ["name", "description", "recursive", "status"]}),
        ("Activities", {"fields": ["assigned_to", "activity_type", "profiles"]}),
        # ("Timestamps", {"fields": ["start_date", "end_date"]}),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class ProcessView(MasterDetailView):
    datamodel = SQLAInterface(LifecycleProfile)
    list_columns = ["name"]  # , "description"] # , "assigned_to", "activities"]
    page_size = 50

    related_views = [ActivityView]

    @expose("/stats")
    def report(self):
        html_content = convert_notebook_to_html("app/reports/resmi-ToDo.ipynb")
        return self.render_template("reports.html", html_content=html_content)


class LifecycleProfileModelView(ModelView):
    datamodel = SQLAInterface(LifecycleProfile)
    list_columns = ["name", "description", "assigned_to", "activities"]
    page_size = 50

    show_fieldsets = [
        ("Main Info", {"fields": ["name", "description", "assigned_to"]}),
        ("Activities", {"fields": ["activities", "assets"]}),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets

    related_views = [ActivityView]


class DetailLifecycleView(MultipleView):
    views = [LifecycleProfileModelView, ActivityView]
