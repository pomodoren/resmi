from flask_appbuilder import ModelView, MasterDetailView, MultipleView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ...models import ConditionType, Condition, MaterialReport, Issue, Event
from .notebooks import convert_notebook_to_html


class ConditionView(ModelView):
    datamodel = SQLAInterface(Condition)
    list_columns = ["name", "description"]


class ConditionTypeView(ModelView):
    datamodel = SQLAInterface(ConditionType)
    list_columns = ["name", "description"]


class MaterialReportView(ModelView):
    datamodel = SQLAInterface(MaterialReport)
    # list_columns = ["name", "description"]
    related_views = [ConditionView]


class ReportView(MasterDetailView):
    datamodel = SQLAInterface(MaterialReport)
    list_columns = ["name"]
    related_views = [ConditionView]


class IssueModelView(ModelView):
    datamodel = SQLAInterface(Issue)
    list_columns = ["name", "description", "severity", "category", "status", "issuer"]

    show_fieldsets = [
        ("Main Info", {"fields": ["name", "description", "severity", "category"]}),
        ("Activities", {"fields": ["status", "response", "issuer"]}),
    ]

    edit_fieldsets = show_fieldsets
    add_fieldsets = show_fieldsets


class EventModelView(ModelView):
    datamodel = SQLAInterface(Event)
    list_columns = ["name", "description", "return_per", "intensity"]


    @expose("/stats")
    def report(self):
        html_content = convert_notebook_to_html("app/reports/resmi-Events.ipynb")
        return self.render_template('reports.html', html_content=html_content)


class DetailReportingView(MultipleView):
    views = [MaterialReportView, ConditionView]
