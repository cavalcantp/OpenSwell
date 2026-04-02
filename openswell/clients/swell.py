"""Swell API client."""
import httpx
from typing import Self
from datetime import datetime
from openswell.core.config import Config

class SwellClient:
    def __init__(
        self: Self,
        config: Config,
    ):
        self.api_key = config.swell_api.api_key
        self.base_url = str(config.swell_api.base_url)

    async def get_swell(
        self: Self,
        lat: float,
        lon: float,
        start: datetime.timestamp,
        end: datetime.timestamp,
    ) -> dict:
        params = {
            "lat": lat,
            "lng": lon,
            "start": start,
            "end": end,
            "params": ",".join([
                "windSpeed",
                "windDirection",
                "swellHeight",
                "swellDirection",
                "swellPeriod",
            ]),
        }

        headers = {
            "Authorization": self.api_key
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.base_url,  
                params=params,
                headers=headers
            )
            response.raise_for_status()

            return response.json()