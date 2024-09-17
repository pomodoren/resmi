from flask_admin import expose, Admin, AdminIndexView

# Define configurations for each module
modules_config = [
    {
        "id": "m1_importers",
        "name": "Importers and Exporters",
        "url": "/m1_data",
        "endpoint": "/m1_data",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m2_portraits",
        "name": "Open Data Portraits",
        "url": "/m2_portraits",
        "endpoint": "/m2_portraits",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m3_assets",
        "name": "My Assets",
        "url": "/m3_assets",
        "endpoint": "/m3_assets",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m4_mobility",
        "name": "Mobility Toolkit",
        "url": "/m4_mobility",
        "endpoint": "/m4_mobility",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m5_fieldwork",
        "name": "Fieldwork",
        "url": "/m5_fieldwork",
        "endpoint": "/m5_fieldwork",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m6_feedback",
        "name": "Infra Feedback",
        "url": "/m6_feedback",
        "endpoint": "/m6_feedback",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m7_events",
        "name": "Events",
        "url": "/m7_events",
        "endpoint": "/m7_events",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    {
        "id": "m8_ai",
        "name": "AI",
        "url": "/m8_ai",
        "endpoint": "/m8_ai",
        "template_mode": "bootstrap2",
        "base_template": "admin/custom_base.html",
    },
    # Add other module configurations here...
]


class DashboardView(AdminIndexView):
    def is_visible(self):
        return False

    @expose("/")
    def index(self):
        return self.render(
            "admin/index.html",
        )


def create_admin_modules():

    # Initialize the dictionary to store admin instances
    dict_admins = {}
    
    # Create and register admin modules
    for config in modules_config:
        admin = Admin(
            name=config["name"],
            template_mode=config["template_mode"],
            index_view=DashboardView(
                url=config["url"], name=config["name"], endpoint=config["endpoint"]
            ),
            base_template=config["base_template"],
            static_url_path='/static'
        )
        # Store admin instance in the dictionary with id as the key
        dict_admins[config["id"]] = admin

    return dict_admins
