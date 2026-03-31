"""Openswell geocoding service"""
from typing import Self
from openswell.clients import GeocodeClient
from openswell.domain.models import Coordinates


class GeocodeService:
    def __init__(
        self: Self,
        client: GeocodeClient,
    ):
        self.client = client

    async def geocode(
        self: Self, 
        location: str,
    ) -> Coordinates:
        data = await self.client.get_geocode(location=location)
    
        if not data:
            raise ValueError("Location not found")

        return Coordinates(lat=float(data[0]["lat"]), lon=float(data[0]["lon"]))