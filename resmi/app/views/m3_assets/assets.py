from ..default_view import NonGeoView


class AssetTypeView(NonGeoView):
    # can_create = False
    column_list = ["id", "name", "created_by", "created_on"]
    can_delete = False
    can_edit = False

    page_size = 100


class AssetView(NonGeoView):
    # can_create = False
    can_delete = False
    can_edit = False
    column_list = ["id", "name", "type", "description"]
    column_sortable_list = ["name", "type", "description"]

    page_size = 100

