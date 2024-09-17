import sys
import os

import pandas as pd
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import BusStop, AssetType

app = create_app()
df = pd.read_csv("../seeder_data/tirana/stops.txt")
df = df.replace({np.nan: None})

with app.app_context():

    stops = BusStop.import_from_gtfs(df)
    for i in stops:
        print(i)
        db.session.add(i)
    db.session.commit()
