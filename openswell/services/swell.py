"""Openswell swell service"""
from pandas import DataFrame
from typing import Self
from datetime import datetime
from openswell.clients import SwellClient
from openswell.domain.models import Swell, Wind, SurfConditions


class SwellService:
    def __init__(
        self: Self,
        client: SwellClient,
    ):
        self.client = client

    async def get_swell(
        self: Self, 
        lat: float, 
        lon: float,
        start: datetime,
        end: datetime,
    ) -> Swell:
        data = await self.client.get_swell(
            lat=lat, 
            lon=lon, 
            start=start.timestamp(),
            end=end.timestamp(),
        )

        df = (
            DataFrame(data=data["hours"])
            .set_index("time")
            .map(lambda x: x["noaa"])
            .mean()
        )

        swell = Swell(
            size=df["swellHeight"],
            direction=df["swellDirection"],
            period=df["swellPeriod"],
        )
        wind = Wind(
            speed=df["windSpeed"],
            direction=df["windDirection"],
        )

        return SurfConditions(
            swell=swell,
            wind=wind,
        )