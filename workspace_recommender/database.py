from pymongo import MongoClient
import pandas as pd
import os

def get_workspace_data():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("❌ MONGO_URI is not set!")
        return None

    client = MongoClient(mongo_uri)
    db = client["workLocate"]
    collection = db["workingspaces"]
    data = list(collection.find())
    df = pd.DataFrame(data)

    df["latitude"] = df["location"].apply(lambda x: x["coordinates"][0] if isinstance(x, dict) else None)
    df["longitude"] = df["location"].apply(lambda x: x["coordinates"][1] if isinstance(x, dict) else None)
    df["amenities_count"] = df["amenities"].apply(lambda x: len(x) if isinstance(x, list) else 0)

    return df[["name", "amenities", "averageRating", "latitude", "longitude", "amenities_count"]]

