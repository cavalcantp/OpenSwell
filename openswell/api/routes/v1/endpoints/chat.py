"""Openswell API chat endpoint defintion."""
from typing import Annotated
from fastapi import APIRouter, Depends
from langchain_core.runnables import Runnable
# from openswell.agents import run_surf_recommender
from openswell.agents import execute_workflow
from openswell.services import GeocodeService, SurfRecommenderService
from openswell.api.schemas import ChatRequest, ChatResponse
from openswell.api.dependencies import fetch_geocode_service, fetch_surf_recommender_llm, fetch_surf_recommender_service

router = APIRouter()

@router.post(
    "",
    response_model=ChatResponse,
    summary="Send your query to the Openswell Surfing Recommender."
)
async def chat(
    chat_request: ChatRequest,
    surf_recommender_llm: Annotated[Runnable, Depends(fetch_surf_recommender_llm)],
    surf_recommender_service: Annotated[SurfRecommenderService, Depends(fetch_surf_recommender_service)],
    geocoding_service: Annotated[GeocodeService, Depends(fetch_geocode_service)],
) -> ChatResponse:
    user_input = chat_request.message
    response = await execute_workflow(
        llm=surf_recommender_llm,
        surf_recommender_service=surf_recommender_service,
        geocoding_service=geocoding_service,
        user_input=user_input
    )
    # response = await run_surf_recommender(agent=surf_recommender_agent, user_input=user_input)
    
    return ChatResponse(message=response["explanation"]["overall_summary"])