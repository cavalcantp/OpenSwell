"""Weather API client defintion."""
import httpx
from datetime import datetime
from typing import Self
from openswell.core.config import Config

class WeatherClient:
    def __init__(self: Self, config: Config):
        self.api_key = config.weather_api.api_key
        self.base_url = str(config.weather_api.base_url)
    
    async def get_weather(
        self: Self,
        lat: float,
        lon:float,
        date: datetime.date,
    ) -> dict:
        params = {
            "lat": lat,
            "long": lon,
            "date": date,
            "appid": self.api_key,
            "units": "metric",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()

            return response.json()