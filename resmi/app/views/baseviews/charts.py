from flask_appbuilder.charts.views import DirectByChartView, GroupByChartView
from flask_appbuilder.models.group import aggregate_avg, aggregate_sum, aggregate_count
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ...models import Asset, MaterialReport



class AssetsChartView(GroupByChartView):
    datamodel = SQLAInterface(Asset)
    chart_title = "Direct Data"

    definitions = [
        {
            "group": "type",
            "series": [(aggregate_count, "id")],
        }
    ]

    
class ReportsChartView(GroupByChartView):
    datamodel = SQLAInterface(MaterialReport)
    chart_title = "Direct Data"

    definitions = [
        {
            "group": "type",
            "series": [(aggregate_count, "id")],
        }
    ]



from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.sqla.filters import FilterEqual
from ...models import Tag

def create_chart_view_for_asset_type(asset_type):
    class DynamicAssetTagGroupByChartView(GroupByChartView):
        datamodel = SQLAInterface(Tag)  # Utilize the Tag model
        chart_title = f'Tag Distribution for {asset_type.name}'

        definitions = [
            {
                'group': 'key',  # Assume 'key' is a field in Tag
                'filters': [
                    ('asset.asset_type_id', FilterEqual, asset_type.id)  # Filter tags by their asset's type
                ],
                'series': [
                    (aggregate_count, 'id')  # Count occurrences of each tag
                ]
            }
        ]

    # Set class name dynamically for unique view registration
    DynamicAssetTagGroupByChartView.__name__ = f"{asset_type.name.replace(' ', '')}TagGroupByChartView"
    return DynamicAssetTagGroupByChartView
