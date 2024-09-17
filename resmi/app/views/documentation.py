from flask import url_for
from wtforms import fields, widgets
from markupsafe import Markup
from flask_admin import form
from flask_admin.contrib import sqla

from .. import file_path


# define a custom wtforms widget and field.
# see https://wtforms.readthedocs.io/en/latest/widgets.html#custom-widgets
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        # add WYSIWYG class to existing classes
        existing_classes = kwargs.pop("class", "") or kwargs.pop("class_", "")
        kwargs["class"] = "{} {}".format(existing_classes, "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class FileView(sqla.ModelView):
    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {"path": form.FileUploadField}

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        "path": {"label": "File", "base_path": file_path, "allow_overwrite": False}
    }


class ImageView(sqla.ModelView):
    def _list_thumbnail(view, context, model, name):
        if not model.path:
            return ""

        return Markup(
            '<img src="%s">'
            % url_for("static", filename=form.thumbgen_filename(model.path))
        )

    column_formatters = {"path": _list_thumbnail}

    # Alternative way to contribute field is to override it completely.
    # In this case, Flask-Admin won't attempt to merge various parameters for the field.
    form_extra_fields = {
        "path": form.ImageUploadField(
            "Image", base_path=file_path, thumbnail_size=(100, 100, True)
        )
    }
