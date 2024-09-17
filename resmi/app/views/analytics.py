from flask_admin import BaseView, expose

class AnalyticsView(BaseView):

    def __init__(self, report_name, *args, **kwargs):
        # Save the report_name to be used in the view
        self.report_name = report_name
        super().__init__(*args, **kwargs)

    @expose("/")
    def index(self):
        print("*" * 10)
        print(self.report_name)
        print("*" * 10)
        voila_url = f"http://localhost:8866/voila/render/{self.report_name}"
        # Render a template, passing the Voilà URL to be used in the iframe
        return self.render("admin/voila.html", voila_url=voila_url, name=self.name)
