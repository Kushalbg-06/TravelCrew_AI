"""
Optional tool: rough travel distance/duration between two places
using the Google Maps Distance Matrix API. Skipped gracefully if no
key is configured.
"""
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from config.settings import settings


class MapsToolInput(BaseModel):
    origin: str = Field(..., description="Starting city")
    destination: str = Field(..., description="Destination city")


class DistanceTool(BaseTool):
    name: str = "Travel Distance Lookup"
    description: str = (
        "Estimates travel distance and duration by road between two cities. "
        "Useful for transport planning."
    )
    args_schema: type[BaseModel] = MapsToolInput

    def _run(self, origin: str, destination: str) -> str:
        if not settings.GOOGLE_MAPS_API_KEY:
            return f"Distance lookup skipped (no GOOGLE_MAPS_API_KEY) for {origin} -> {destination}."

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "key": settings.GOOGLE_MAPS_API_KEY,
        }
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            element = data["rows"][0]["elements"][0]
            if element.get("status") != "OK":
                return f"No route data for {origin} -> {destination}."
            distance = element["distance"]["text"]
            duration = element["duration"]["text"]
            return f"{origin} to {destination}: {distance}, approx {duration} by road."
        except Exception as e:
            return f"Distance lookup failed: {e}"
