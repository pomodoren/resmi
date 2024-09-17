from . import assets as aa
from . import fieldwork as la

from . import charts as cha
from . import documentation as docs
from . import reporting as ra

from ... import appbuilder

# Modules

appbuilder.add_link(name="M1. Open Data Portraits", href="m2_portraits", category="Modules")
appbuilder.add_link(name="M2. Importers and Exporters", href="m1_importers", category="Modules")
appbuilder.add_separator(category="Modules")
appbuilder.add_link(name="M3. My Assets", href="m3_assets", category="Modules")
appbuilder.add_link(name="M4. Mobility Toolkit", href="m4_mobility", category="Modules")
appbuilder.add_separator(category="Modules")
appbuilder.add_link(name="M5. Fieldwork", href="m5_fieldwork", category="Modules")
appbuilder.add_link(name="M6. Issues", href="m6_feedback", category="Modules")
appbuilder.add_separator(category="Modules")
appbuilder.add_link(name="M7. Events", href="m7_events", category="Modules")
appbuilder.add_link(name="M8. AI", href="m8_ai", category="Modules")

appbuilder.add_separator(category="Modules")

# OTHER STUFF TO BE REFACTORED
appbuilder.add_link(name=" ", href="#")
appbuilder.add_link(name=" ", href="#")

appbuilder.add_view(
    aa.AssetTypeView,
    name="Asset Types",
    category_icon="fa-file-text-o",
    category="Configuration",
)
appbuilder.add_separator(category="Configuration")
appbuilder.add_view(
    ra.ConditionTypeView, name="Condition Types", category="Configuration"
)
appbuilder.add_view(aa.StandardTagView, name="Standard Tags", category="Configuration")
appbuilder.add_view(
    aa.AllowedTagValueView, name="Allowed Tags", category="Configuration"
)

appbuilder.add_separator(category="Configuration")
appbuilder.add_view(
    la.ActivityTypesView, name="Activity Types", category="Configuration"
)
appbuilder.add_view(la.CostTypeView, name="Cost Type", category="Configuration")

# DOCUMENTATION

appbuilder.add_link(
    "Documentation",
    href="file:///home/pomodoren/Desktop/SUTi/ResMI/docs/_build/html/intro.html",
    category_icon="fa-file-text-o",
    category="Documentation",
)

appbuilder.add_separator(category="Documentation")
appbuilder.add_view(
    docs.FileView,
    name="Legislation Files",
    category_icon="fa-file-text-o",
    category="Documentation",
)
appbuilder.add_view(docs.ImageView, name="Images", category="Documentation")

appbuilder.add_link(
    "API",
    href="file:///home/pomodoren/Desktop/SUTi/ResMI/docs/_build/html/intro.html",
    category_icon="fa-file-text-o",
    category="API",
)

