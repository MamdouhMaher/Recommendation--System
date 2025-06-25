
from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend_nearby

print("🚀 FastAPI app is starting...")

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Location(BaseModel):
    latitude: float
    longitude: float

@app.get("/")
def home():
    return {"status": "API is running!"}

@app.post("/recommend")
def recommend(location: Location):
    print(f"📍 Received: lat={location.latitude}, lon={location.longitude}")
    results = recommend_nearby(location.latitude, location.longitude)
    return results.to_dict(orient="records")

