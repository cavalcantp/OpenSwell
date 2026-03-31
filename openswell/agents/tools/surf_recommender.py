"""Openswell surf recommender tool defintion."""
from langchain_core.tools import tool, BaseTool
from openswell.services import SurfRecommenderService
from openswell.domain.models import SurferPreferences


def create_surf_recommendation_tool(
    surf_recommender: SurfRecommenderService,
) -> BaseTool:
    @tool(
        name_or_callable="generate_surf_recommendations",
        description="Generate surf recommendations based on location and surfer preferences",
    )
    async def generate_surf_recommendations(
        lat: float,
        lon: float,
        surfer_preferences: SurferPreferences,
    ):
        return await surf_recommender.generate_surf_recommendations(
            lat=lat,
            lon=lon,
            surfer_preferences=surfer_preferences,
        )

    return generate_surf_recommendations