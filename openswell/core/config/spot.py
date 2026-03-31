"""Spot DB configuration defintion."""
from pydantic import BaseModel
from pathlib import Path

class SpotStoreConfig(BaseModel):
    path: Path = Path.cwd().joinpath("openswell/data/surf_spots.json")