from .public_transport import BusStopView
from ..default_view import OSMAssetView
from ..analytics import AnalyticsView
from ... import dict_admins, db, models

admin = dict_admins["m4_mobility"]

admin.add_view(
    BusStopView(
        models.BusStop, db.session, name="Bus Stops", category="Public Transport"
    )
)

for model in [
    models.Bench,
    models.Bin,
    models.TimetableInfo,
    models.Advertisement,
    models.BusStopSign,
]:
    admin.add_view(
        OSMAssetView(
            model,
            db.session,
            name=str(model.name).replace(".name", ""),
            category="Public Transport",
        )
    )

for model in [
    models.CyclingPath,
    models.CyclingAsset,
]:
    admin.add_view(
        OSMAssetView(
            model,
            db.session,
            name=str(model.name).replace(".name", ""),
            category="Cycling",
        )
    )

for model in [
    models.Sidewalk,
    models.Crossing,
]:
    admin.add_view(
        OSMAssetView(
            model,
            db.session,
            name=str(model.name).replace(".name", ""),
            category="Walking",
        )
    )

for model in [models.TaxiStations, models.ChargingStation, models.Parking]:
    admin.add_view(
        OSMAssetView(
            model,
            db.session,
            name=str(model.name).replace(".name", ""),
            category="Parking & Stations",
        )
    )

for model in [models.Road, models.RoadSegment, models.TrafficSignal]:
    admin.add_view(
        OSMAssetView(
            model,
            db.session,
            name=str(model.name).replace(".name", ""),
            category="Road Infrastructure",
        )
    )
