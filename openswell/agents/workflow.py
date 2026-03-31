from typing import Any
from langchain_core.runnables import Runnable
from openswell.agents.intent_extractor import extract_intent
from openswell.agents.explainer import explain_recommendations
from openswell.services import SurfRecommenderService, GeocodeService


async def execute_workflow(
    llm: Runnable,
    surf_recommender_service: SurfRecommenderService,
    geocoding_service: GeocodeService,
    user_input: str,
) -> dict[str, Any]:
    # 1. Extract intent
    intent = await extract_intent(llm=llm, user_input=user_input)

    # 2. Geocode
    coordinates = await geocoding_service.geocode(location=intent.location)

    # 3. Call recommendation service
    recommendations = await surf_recommender_service.generate_surf_recommendations(
        lat=coordinates.lat,
        lon=coordinates.lon,
        session_time=intent.session_time,
        surfer_preferences=intent.surfer_preferences,
    )

    # 4. Explain
    explanation = await explain_recommendations(
        llm=llm,
        user_input=user_input,
        results=recommendations,
    )

    return {
        "intent": intent.model_dump(),
        "recommendations": [recomendation.model_dump() for recomendation in recommendations],
        "explanation": explanation.model_dump(),
    }