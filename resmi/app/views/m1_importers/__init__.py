from .importers_osm import OSMImporterView, BaseImporterView
from ... import dict_admins

# Modules
admin = dict_admins["m1_importers"]

admin.add_view(OSMImporterView(name="OSM Importer", endpoint="osm_importer"))
admin.add_view(BaseImporterView(name="GTFS Importer", endpoint="gtfs_importer"))
admin.add_view(BaseImporterView(name="GBFS Importer", endpoint="gbfs_importer"))
admin.add_view(BaseImporterView(name="Excel Importer", endpoint="excel_importer"))
