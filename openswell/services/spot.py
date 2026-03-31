"""Openswell spot service defintion."""
import json
from typing import Self
from openswell.core.config import Config
from openswell.domain.models import SurfSpot

class SpotService:
    def __init__(
        self: Self,
        config: Config
    ):
        with open(config.spot_store.path) as file:
            data = json.load(file)

            self.spots = [SurfSpot.model_validate(spot) for spot in data]

    def fetch_spots(self: Self):
        return self.spots
    