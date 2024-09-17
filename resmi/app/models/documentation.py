import os
from sqlalchemy.event import listens_for
from flask_admin import form
from flask import Markup, url_for

from PIL import Image as ImagePIL  # noqa

from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship

from flask_appbuilder import Model
from flask_appbuilder.filemanager import ImageManager, FileManager
from flask_appbuilder.models.mixins import ImageColumn, FileColumn

from .. import db, file_path, op
from .mixins import AuditMixinNullable


class File(db.Model, AuditMixinNullable):  # , DBMixin):
    __tablename__ = "files"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(Unicode(64))
    file = Column(FileColumn, nullable=False)

    activity_id = Column(Integer, ForeignKey("lifecycle_activities.id"))
    activity = relationship("LifecycleActivity")

    def __unicode__(self):
        return self.name

    def download(self):
        return Markup(
            '<a href="'
            + url_for("FileModelView.download", filename=str(self.file))
            + '">Download</a>'
        )


class Image(db.Model, AuditMixinNullable):  # , DBMixin):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Unicode(64))
    photo = Column(ImageColumn(size=(100, 100, True), thumbnail_size=(30, 30, True)))

    asset_id = db.Column(db.Integer, db.ForeignKey("assets.id"))
    asset = db.relationship("Asset", back_populates="images")

    def __unicode__(self):
        return self.name

    def photo_img(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="'
                + url_for("ImageView.show", pk=str(self.id))
                + '" class="thumbnail"><img src="'
                + im.get_url(self.photo)
                + '" alt="Photo" class="img-rounded img-responsive"></a>'
            )
        else:
            return Markup(
                '<a href="'
                + url_for("ImageView.show", pk=str(self.id))
                + '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>'
            )

    def photo_img_thumbnail(self):
        im = ImageManager()
        if self.photo:
            return Markup(
                '<a href="'
                + url_for("ImageView.show", pk=str(self.id))
                + '" class="thumbnail"><img src="'
                + im.get_url_thumbnail(self.photo)
                + '" alt="Photo" class="img-rounded img-responsive"></a>'
            )
        else:
            return Markup(
                '<a href="'
                + url_for("ImageView.show", pk=str(self.id))
                + '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>'
            )


# Delete hooks for models, delete files if models are getting deleted
@listens_for(File, "after_delete")
def del_file(mapper, connection, target):
    if target.path:
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


@listens_for(Image, "after_delete")
def del_image(mapper, connection, target):
    if target.path:
        # Delete image
        try:
            os.remove(op.join(file_path, target.path))
        except OSError:
            pass

        # Delete thumbnail
        try:
            os.remove(op.join(file_path, form.thumbgen_filename(target.path)))
        except OSError:
            pass
