"""Geocode API client."""
import httpx
from typing import Self
from openswell.core.config import Config
from openswell.domain.models import Coordinates

class GeocodeClient:
    def __init__(
        self: Self,
        config: Config,
    ):
        self.base_url = str(config.geocode_api.base_url)

    async def get_geocode(
        self: Self,
        location: str,
    ) -> Coordinates:
        params = {
            "q": location,
            "format": "json",
            "limit": 1,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            
            return response.json()

        