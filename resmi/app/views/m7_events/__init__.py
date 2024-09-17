from ... import dict_admins, db, models

from .events import EventView

admin = dict_admins["m7_events"]

admin.add_view(
    EventView(models.HazardEvent, db.session, name="Hazards")
)
