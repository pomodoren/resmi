import logging
import os
import os.path as op

from flask import Flask
from flask import redirect, render_template

from flask_appbuilder import AppBuilder, SQLA
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify, abort

from sqlalchemy.engine import Engine
from sqlalchemy import event

from flask_admin import expose, Admin, AdminIndexView
from flask_restful import Api
from flask_cors import CORS

from flask_appbuilder import IndexView, BaseView
from flask_appbuilder.menu import Menu
from .init_modules import create_admin_modules


# from .views.appbuilder_views.index_view import MyIndexView
class MyIndexView(IndexView):
    index_template = "my_index.html"
    base_template = "base_template.html"


class MyIndexView2(BaseView):

    route_base = "base"
    default_view = "main"
    index_template = "my_index.html"
    base_template = "base_template.html"


# Initialize extensions
db = SQLA()
ma = Marshmallow()
appbuilder = AppBuilder(
    indexview=MyIndexView, menu=Menu(), base_template="base_template.html"
)

# admins
dict_admins = create_admin_modules()
admin_importers = dict_admins["m1_importers"]
admin = dict_admins["m3_assets"]
admin_issues = dict_admins["m6_feedback"]

restful_api = Api()
cors = CORS()


# Create directory for file fields to use
file_path = op.join(op.dirname(__file__), "files")
try:
    os.mkdir(file_path)
except OSError:
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    app.config["CORS_HEADERS"] = "Content-Type,Authorization,Options"
    app.config["FLASK_ADMIN_SWATCH"] = "cosmo"

    # Initialize extensions
    db.init_app(app)

    cors.init_app(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "X-Custom-Header", "Authorization", "Options"],
    )

    # Function to load SpatiaLite extension
    def load_spatialite(dbapi_conn, connection_record):
        dbapi_conn.enable_load_extension(True)
        dbapi_conn.load_extension("mod_spatialite")  # Adjust the path as necessary

    # Set up event listener to load SpatiaLite extension when a new SQLite connection is created
    @event.listens_for(Engine, "connect")
    def provide_engine_connection(dbapi_connection, connection_record):
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith(
            "sqlite"
        ):  # Check if using SQLite
            load_spatialite(dbapi_connection, connection_record)

    with app.app_context():

        appbuilder.init_app(app, db.session)
        # appbuilder_assets.init_app(app, db.session)
        for val in dict_admins.values():
            val.init_app(app)
       
        restful_api.init_app(app)

        from . import views

        # db.drop_all()
        db.create_all()

        from .models import BusStop, AssetType
        from flask_admin import BaseView
        from flask import render_template

        # from .utils import wkb_to_geojson
        from sqlalchemy import func

        class DashboardView(BaseView):

            def is_visible(self):
                return False

            @expose("/")
            def index(self):
                items = db.session.query(
                    BusStop.id,
                    BusStop.description,
                    func.ST_AsGeoJSON(BusStop.geometry).label("geometry"),
                ).all()
                return self.render("admin/index.html", items=items)

        dict_admins["m1_importers"].add_view(DashboardView(name="index"))

        @app.route("/")
        def index():
            items = db.session.query(
                BusStop.id,
                BusStop.description,
                func.ST_AsGeoJSON(BusStop.geometry).label("geometry"),
            ).all()
            return render_template("index.html", items=items)

    return app


if __name__ == "__main__":
    app = create_app()  # Adjust your configuration accordingly
    app.run(debug=True)
