"""Openswell recommender service defintion."""
from typing import Self
from datetime import datetime
from openswell.domain.models import SurfSpot, SurfConditions, SurferPreferences, Recommendation, SurfConditions, SessionTime
from openswell.services.swell import SwellService
from openswell.services.weather import WeatherService
from openswell.services.spot import SpotService
from timezonefinder import TimezoneFinder
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from openswell.domain.models import SessionTime

class SurfRecommenderService:
    def __init__(
        self: Self,
        swell_service: SwellService,
        weather_service: WeatherService,
        spot_service: SpotService,
    ):
        self.swell_service = swell_service
        self.weather_service = weather_service
        self.spot_service = spot_service
        self.tf = TimezoneFinder()


    async def generate_surf_recommendations(
        self: Self,
        lat: float,
        lon: float,
        session_time: SessionTime,
        surfer_preferences: SurferPreferences,
    ) -> list[Recommendation]:
        # wind = await self.weather_service.get_wind(lat=lat, lon=lon, date=date)
        start, end = self._estimate_session_start_and_end(
            session_time=session_time,
            tz=self.tf.timezone_at(lat=lat, lng=lon)
        )
        surf_conditions = await self.swell_service.get_swell(
            lat=lat, 
            lon=lon, 
            start=start,
            end=end,
        )

        spots = self.spot_service.fetch_spots()

        ranked = self.rank_spots(
            spots=spots, 
            surf_conditions=surf_conditions,
            # surfer_preferences=surfer_preferences,
        )

        return ranked[:3] #[r.model_dump() for r in ranked[:3]]
    

    def rank_spots(
        self: Self,
        spots: list[SurfSpot],
        surf_conditions: SurfConditions,
        # surfer_preferences: SurferPreferences,
    ) -> list[Recommendation]:
        results = [self.score_spot(spot=spot, surf_conditions=surf_conditions) for spot in spots]

        return sorted(results, key=lambda x: x.score, reverse=True)
    

    def score_spot(
        self: Self,
        spot: SurfSpot,
        surf_conditions: SurfConditions,
    ) -> Recommendation:
        # TODO: take surfer preferences into consideration ?
        score = 0
        breakdown = {}

        # Swell size scoring
        swell_size = surf_conditions.swell.size
        min_swell_size, max_swell_size = spot.optimal_swell_size
        swell_size_score = 5 if min_swell_size <= swell_size <= max_swell_size else -3
        breakdown["swell_size"] = swell_size_score
        score += swell_size_score

        # Swell direction scoring
        swell_direction_diff = abs(surf_conditions.swell.direction - (spot.optimal_swell_direction or 0))
        swell_direction_score = max(0, 5 - swell_direction_diff/60)
        breakdown["swell_direction"] = swell_direction_score
        score += swell_direction_score

        # Wind direction scoring
        wind_direction_diff = abs(surf_conditions.wind.direction - (spot.optimal_wind_direction or 0))
        wind_direction_score = max(0, 3 - wind_direction_diff/60)
        breakdown["wind_direction_score"] = wind_direction_score
        score += wind_direction_score

        # Wind intensity score
        wind_speed_score = 1 / surf_conditions.wind.speed
        breakdown["wind_speed_score"] = wind_direction_score
        score += wind_speed_score

        return Recommendation(
            spot=spot,
            score=score,
            swell_size=swell_size,
            swell_direction=surf_conditions.swell.direction,
            wind_speed=surf_conditions.wind.speed,
            wind_direction=surf_conditions.wind.direction,
            score_breakdown=breakdown,
        )


    def _estimate_session_start_and_end(
        self,
        session_time: SessionTime,
        tz: str = "Europe/Lisbon",
    ) -> tuple[datetime, datetime]:
        now = datetime.now(ZoneInfo(tz))
        today = now.date()

        if session_time == SessionTime.MORNING:
            start = datetime.combine(today, time(8, 0), tzinfo=ZoneInfo(tz))
            end = datetime.combine(today, time(11, 0), tzinfo=ZoneInfo(tz))
        else:
            start = datetime.combine(today, time(14, 0), tzinfo=ZoneInfo(tz))
            end = datetime.combine(today, time(17, 0), tzinfo=ZoneInfo(tz))

        return start, end