from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from ...models import File, Image


class FileView(ModelView):
    datamodel = SQLAInterface(File)
    list_columns = ["name", "file", "activity"]


class ImageView(ModelView):
    datamodel = SQLAInterface(Image)
    label_columns = {
        "name": "Name",
        "photo": "Photo",
        "photo_img": "Photo",
        "photo_img_thumbnail": "Photo",
    }
    list_columns = ["name", "asset", "photo_img"]

    show_fieldsets = [
        (
            "Main Info",
            {"fields": ["name"]},
        ),
        (
            "Photo",
            {
                "fields": [
                    "photo",
                ]
            },
        ),
        (
            "Related",
            {
                "fields": [
                    "asset",
                ]
            },
        ),
    ]

    edit_fieldsets = [
        (
            "Main Info",
            {"fields": ["name", "photo"]},
        ),
        (
            "Related",
            {
                "fields": [
                    "asset",
                ]
            },
        ),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets
