from flask_appbuilder import ModelView, MasterDetailView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from flask import render_template

from ...models import Relation, AssetType, Asset, Tag, StandardTag, AllowedTagValue
from .notebooks import convert_notebook_to_html
from .documentation import ImageView


class TagView(ModelView):
    datamodel = SQLAInterface(Tag)
    list_columns = ["id", "key", "value", "active", "asset", "asset.asset_type"]
    page_size = 100

    show_fieldsets = [
        ("Main Info", {"fields": ["key", "value"]}),
        ("Baseline", {"fields": ["active", "value_type"]}),
        ("Related", {"fields": ["asset", "standard_tag"]}),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class StandardTagView(ModelView):
    datamodel = SQLAInterface(StandardTag)
    list_columns = ["id", "key", "description", "asset_type", "allowed_values"]
    page_size = 100

    show_fieldsets = [
        ("Main Info", {"fields": ["key", "description"]}),
        ("Related", {"fields": ["asset_type", "allowed_values"]}),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class AllowedTagValueView(ModelView):
    datamodel = SQLAInterface(StandardTag)
    list_columns = ["id", "key", "value", "active"]
    page_size = 100


class AssetView(ModelView):
    datamodel = SQLAInterface(Asset)
    list_columns = [
        "id",
        "name",
        "asset_type",
        "public",
        "description",
        "vid",
        "changed_on",
        "created_on",
    ]
    page_size = 100

    related_views = [TagView, ImageView]

    show_fieldsets = [
        (
            "Main Info",
            {"fields": ["name", "description", "public", "active", "asset_type"]},
        ),
        ("Other Info", {"fields": ["osm_id", "vid", "vid_version"]}),
        (
            "Related",
            {
                "fields": [
                    "issues",
                    "events",
                    "material_reports",
                    "lifecycle_profiles",
                ]
            },
        ),
        ("Meta", {"fields": ["created_by", "created_on", "changed_by", "changed_on"]}),
    ]

    edit_fieldsets = [
        (
            "Main Info",
            {"fields": ["name", "description", "public", "active", "asset_type"]},
        ),
        ("Other Info", {"fields": ["osm_id", "vid", "vid_version"]}),
        (
            "Related",
            {
                "fields": [
                    "issues",
                    "events",
                    "material_reports",
                    "lifecycle_profiles",
                ]
            },
        ),
    ]
    add_fieldsets = edit_fieldsets

    @expose("/stats")
    def report(self):
        html_content = convert_notebook_to_html("app/reports/resmi-Assets.ipynb")
        return self.render_template("reports.html", html_content=html_content)


class AssetTagsView(MasterDetailView):
    datamodel = SQLAInterface(Asset)
    list_columns = ["name"]  # , "assigned_to", "activities"]
    page_size = 100

    related_views = [TagView]


class AssetTypeView(ModelView):
    datamodel = SQLAInterface(AssetType)
    list_columns = ["id", "name", "description", "asset_type_group"]
    can_delete = False
    page_size = 50


class RelationView(ModelView):
    datamodel = SQLAInterface(Relation)
    list_columns = ["name", "public", "description"]
    page_size = 50
