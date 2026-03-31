"""Openswell API dependency injectors."""
from typing import Annotated
from fastapi import Depends, Request
from langchain_core.runnables import Runnable
from openswell.core.config import Config
from openswell.services import GeocodeService, SurfRecommenderService

async def fetch_lifespanstate(request:Request) -> dict:
    return request.app.state

async def fetch_config(
    state: Annotated[dict, Depends(fetch_lifespanstate)]
) -> Config:
    return state.config

async def fetch_geocode_service(
    state: Annotated[dict, Depends(fetch_lifespanstate)],
) -> GeocodeService:
    return state.geocode_service

async def fetch_surf_recommender_llm(
    state: Annotated[dict, Depends(fetch_lifespanstate)]
) -> Runnable:
    return state.surf_recommender_llm

async def fetch_surf_recommender_service(
    state: Annotated[SurfRecommenderService, Depends(fetch_lifespanstate)],
) -> SurfRecommenderService:
    return state.surf_recommender_service

# async def fetch_surf_recommender_agent(
#     state: Annotated[dict, Depends(fetch_lifespanstate)]
# ) -> Runnable:
#     return state.surf_recommender_agent