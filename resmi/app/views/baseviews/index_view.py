from flask_appbuilder import IndexView
from flask_appbuilder.views import expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ...models import AssetType, Asset, Tag


class MyIndexView(IndexView):
    index_template = "my_index.html"
    datamodel = SQLAInterface(Asset)

    @expose("/")
    def index(self):
        self.update_redirect()
        assets = self.datamodel.session.query(Asset).order_by(Asset.id).all()
        return self.render_template(
            self.index_template, assets=assets, appbuilder=self.appbuilder
        )
