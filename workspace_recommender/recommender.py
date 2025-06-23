from geopy.distance import geodesic
from database import get_workspace_data

def recommend_nearby(user_lat, user_lon, top_n=5):
    df = get_workspace_data()

    df = df.dropna(subset=["latitude", "longitude"])
    df["distance"] = df.apply(
        lambda row: geodesic((user_lat, user_lon), (row["latitude"], row["longitude"])).km,
        axis=1
    )

    top_results = df.sort_values(by="distance").head(top_n)
    return top_results
