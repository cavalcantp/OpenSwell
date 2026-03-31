"""Openswell weather service defintion."""
from typing import Self
from datetime import datetime
from openswell.clients import WeatherClient
from openswell.domain.models import Wind

class WeatherService:
    def __init__(
        self: Self,
        client: WeatherClient,
    ):
        self.client = client

    async def get_wind(
        self: Self,
        lat: float,
        lon: float,
        date: datetime.date,
    ) -> Wind:
        data = await self.client.get_weather(lat=lat, lon=lon, date=date)

        return Wind(
            speed=data["wind"]["speed"],
            direction=data["wind"]["deg"],
        )
    