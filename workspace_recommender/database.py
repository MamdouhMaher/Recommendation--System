from pymongo import MongoClient
import pandas as pd
import os

def extract_lat_lon(location, index):
    if isinstance(location, dict):
        coords = location.get("coordinates")
        if isinstance(coords, list) and len(coords) == 2:
            return coords[index]
    return None

def get_workspace_data():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        print("❌ MONGO_URI is not set!")
        return pd.DataFrame()  # Return empty dataframe instead of None

    client = MongoClient(mongo_uri)
    db = client["workLocate"]
    collection = db["workingspaces"]
    data = list(collection.find())
    df = pd.DataFrame(data)

    # ✅ SAFELY extract coordinates
    def extract_lat(x):
        if isinstance(x, dict) and "coordinates" in x:
            coords = x["coordinates"]
            if isinstance(coords, list) and len(coords) >= 2:
                return coords[0]
        return None

    def extract_lon(x):
        if isinstance(x, dict) and "coordinates" in x:
            coords = x["coordinates"]
            if isinstance(coords, list) and len(coords) >= 2:
                return coords[1]
        return None

    df["latitude"] = df["location"].apply(extract_lat)
    df["longitude"] = df["location"].apply(extract_lon)

    df["amenities_count"] = df["amenities"].apply(lambda x: len(x) if isinstance(x, list) else 0)

    return df[[
        "_id", "name", "amenities", "averageRating",
        "latitude", "longitude", "amenities_count", "image"
    ]]


    # Optional debug info: print how many rows were skipped due to invalid coordinates
    missing = df[["latitude", "longitude"]].isnull().any(axis=1).sum()
    print(f"⚠️ Skipped {missing} rows with missing or invalid coordinates")

    # Drop rows that are still missing lat/lon after extraction
    df.dropna(subset=["latitude", "longitude"], inplace=True)

    return df[["name", "amenities", "averageRating", "latitude", "longitude", "amenities_count","image"]]

