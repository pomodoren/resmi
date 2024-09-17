import sys
import os

import pandas as pd
import numpy as np
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db, models
from sqlalchemy.exc import IntegrityError


sheet_to_model = [
    models.AssetType,
    models.Relation,
    models.LifecycleActivityType,
    models.LifecycleProfile,
    models.LifecycleActivity,
    models.m5_fieldwork.lifecycle_profile_activity_association,
    models.m5_fieldwork.CostType,
    models.m5_fieldwork.Cost,
]

sheet_to_model_name = [
    # 'ab_user',
    "asset_types",
    "relations",
    "lifecycle_activity_types",
    "lifecycle_profiles",
    "lifecycle_activities",
    "lifecycle_profile_activity_asso",
    "cost_types",
    "costs",
]

# Load Excel file
excel_file = "../seeder_data/tirana/2024_05_AssetManagement_Settings_Costs.xlsx"


# Function to convert Excel dates and pandas Timestamps to datetime objects
def convert_date(date_value):
    if pd.isna(date_value):
        return None
    elif isinstance(date_value, pd.Timestamp):
        return date_value.to_pydatetime()  # Convert pandas Timestamp to Python datetime
    elif isinstance(date_value, str):
        try:
            return datetime.strptime(
                date_value, "%Y-%m-%d"
            )  # Adjust format as necessary
        except ValueError:
            return None
    return date_value


# Function to seed data from an Excel sheet
def seed_data_from_sheet(df, model):
    print(model)
    if model in [models.m5_fieldwork.lifecycle_profile_activity_association]:
        print(df)
        for index, row in df.iterrows():
            "Entered"
            try:
                db.session.execute(model.insert().values(**row.to_dict()))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print(e)
        return
    for index, row in df.iterrows():
        if "id" in row:
            row = row.drop("id")
        record = model(**row.to_dict())

        try:
            db.session.add(record)
            db.session.commit()
        except IntegrityError as e:
            print(e)
            db.session.rollback()


app = create_app()

with app.app_context():

    for i, model in enumerate(sheet_to_model):
        print(i)
        sheet_name = sheet_to_model_name[i]
        try:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            if "id" in df.columns:
                df = df.drop(columns=["id"])
            df = df.replace({np.nan: None})
        except Exception as e:
            print(e)
            continue
        seed_data_from_sheet(df, model)
