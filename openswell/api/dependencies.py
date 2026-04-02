"""Openswell API dependency injectors."""
from typing import Annotated
from fastapi import Depends, Request
from langchain_core.runnables import Runnable
from openswell.core.config import Config
from openswell.services import GeocodeService, SurfRecommenderService

async def get_lifespanstate(request:Request) -> dict:
    return request.app.state

async def get_config(
    state: Annotated[dict, Depends(get_lifespanstate)]
) -> Config:
    return state.config

async def get_geocode_service(
    state: Annotated[dict, Depends(get_lifespanstate)],
) -> GeocodeService:
    return state.geocode_service

async def get_surf_recommender_llm(
    state: Annotated[dict, Depends(get_lifespanstate)]
) -> Runnable:
    return state.surf_recommender_llm

async def get_surf_recommender_service(
    state: Annotated[SurfRecommenderService, Depends(get_lifespanstate)],
) -> SurfRecommenderService:
    return state.surf_recommender_service

# async def get_surf_recommender_agent(
#     state: Annotated[dict, Depends(get_lifespanstate)]
# ) -> Runnable:
#     return state.surf_recommender_agent