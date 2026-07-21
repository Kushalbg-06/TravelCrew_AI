"""
CrewAI tool wrapping the OpenWeatherMap current-weather endpoint.
"""
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from config.settings import settings


class WeatherToolInput(BaseModel):
    city: str = Field(..., description="City name to check current weather for")


class WeatherTool(BaseTool):
    name: str = "Weather Lookup"
    description: str = (
        "Fetches the current weather (condition, temperature, humidity) "
        "for a given destination city. Input is a city name."
    )
    args_schema: type[BaseModel] = WeatherToolInput

    def _run(self, city: str) -> str:
        if not settings.WEATHER_API_KEY:
            return f"Weather data unavailable (no API key configured) for {city}."

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": settings.WEATHER_API_KEY, "units": "metric"}
        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            condition = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            return f"{city}: {condition}, {temp}°C, humidity {humidity}%."
        except Exception as e:
            return f"Could not fetch weather for {city}: {e}"
