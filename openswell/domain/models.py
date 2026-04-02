"""Openswell domain object model deifintions."""
from typing import List, Optional, Tuple
from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel, Field

class Coordinates(BaseModel):
    lat: float
    lon: float

class SkillLevel(StrEnum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"
    PRO = "PRO"

class Stance(StrEnum):
    REGULAR = "REGULAR"
    GOOFY = "GOOFY"
    BOTH = "BOTH"
    UNKNOWN = "UNKNOWN"

class Wind(BaseModel):
    speed: float  = Field(description="Wind speed in m/s.")
    direction: float = Field(description="Wind direction in degress 0-360.")


class Swell(BaseModel):
    size: float  = Field(description="Wave size in feet.")
    direction: float  = Field(description="Swell direction in degress.")
    period: float  = Field(description="Swell period in seconds.")


class SurfSpot(BaseModel):
    name: str
    coordinates: Coordinates
    min_skill_level: SkillLevel = Field(description="Mininum skill level required to surf the spot.")

    # Ideal conditions for the spot
    optimal_swell_size: Tuple[float, float]  # (min, max) in meters
    optimal_swell_direction: float | None = None  # degrees
    optimal_wind_direction: float | None = None  # offshore direction

    # Optional metadata
    description: Optional[str] = None


class SurfConditions(BaseModel):
    """Aggregated environmental conditions for a location/time."""
    wind: Wind
    swell: Swell

class SurferPreferences(BaseModel):
    skill_level: SkillLevel
    max_swell_size: float | None = None
    preferred_swell_size: Tuple[float, float] | None = None
    goal: str | None = None
    stance: Stance = Stance.UNKNOWN
    avoid_crowds: bool | None = False


class Recommendation(BaseModel):
    spot: SurfSpot
    score: float = Field(..., description="Computed score for ranking")
    swell_size: float
    swell_direction: float
    wind_speed: float
    wind_direction: float

    # Optional debug info
    score_breakdown: dict | None = None


class RecommendationResult(BaseModel):
    location: Coordinates
    recommendations: List[Recommendation]

class SessionTime(StrEnum):
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"

class SurfIntent(BaseModel):
    location: str
    session_time: SessionTime = SessionTime.MORNING
    surfer_preferences: SurferPreferences

class SpotExplanation(BaseModel):
    name: str
    summary: str
    swell_analysis: str
    wind_analysis: str
    suitability_analysis: str
    summary: str


class ExplanationResponse(BaseModel):
    spots: List[SpotExplanation]
    overall_summary: str