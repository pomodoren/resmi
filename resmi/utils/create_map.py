import requests
import json

import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx


def overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    response = requests.get(url, params={"data": query})
    return response.json()


# Query for bus stops in Tiranë
query_bus_stops = """
[out:json][timeout:50];
area["name"="Tiranë"]->.searchArea;
(
  node["amenity"="parking"](area.searchArea);
  way["amenity"="parking"](area.searchArea);
  relation["amenity"="parking"](area.searchArea);
);
out body;>;out skel qt;
{{style:
  node[amenity=parking][parking=surface] { color:black; symbol-size:10; }
  node[amenity=parking][parking=multi-storey] { color:blue; symbol-size:10; }
  node[amenity=parking][parking=underground] { color:darkblue; symbol-size:10; }
  node[amenity=parking][disabled=yes] { color:red; symbol-size:10; }
  way[amenity=parking][parking=surface] { color:yellow; width:3; }
  way[amenity=parking][parking=multi-storey] { color:blue; width:3; }
  way[amenity=parking][parking=underground] { color:darkblue; width:3; }
  way[amenity=parking][disabled=yes] { color:red; width:3; }
  relation[amenity=parking][parking=surface] { color:yellow; width:3; }
  relation[amenity=parking][parking=multi-storey] { color:blue; width:3; }
  relation[amenity=parking][parking=underground] { color:darkblue; width:3; }
  relation[amenity=parking][disabled=yes] { color:red; width:3; }
}}
"""


def create_map(data):
    # Extract coordinates from the data
    coords = [(element["lon"], element["lat"]) for element in data["elements"]]

    # Convert to GeoDataFrame
    gdf = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(
            [lon for lon, lat in coords], [lat for lon, lat in coords]
        )
    )

    # Set the coordinate system to WGS84 and then to Web Mercator for contextily
    gdf.crs = "epsg:4326"
    gdf = gdf.to_crs(epsg=3857)

    # Plotting
    ax = gdf.plot(
        figsize=(10, 10), alpha=0.5, edgecolor="k", color="blue", markersize=50
    )
    ctx.add_basemap(ax)  #  source=ctx.providers.Stamen.TonerLite)
    ax.set_axis_off()

    # Save as PNG
    plt.savefig("tirana_bus_stops.png", dpi=300)
    plt.show()


# Fetch data
try:
    data_bus_stops = overpass_query(query_bus_stops)
except:
    print("ENTERED")
    with open("geo_cycling.geojson") as f:
        data_bus_stops = json.load(f)
    print(data_bus_stops)

# Create map
if data_bus_stops:
    create_map(data_bus_stops)
    print("Map has been created and saved as 'tirana_bus_stops.png'.")
else:
    print("Failed to fetch data.")
