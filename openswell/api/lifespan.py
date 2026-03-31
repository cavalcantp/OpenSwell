"""Openswell API lifespan state management."""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from openswell.core.config import Config
from openswell.clients import SwellClient, WeatherClient, GeocodeClient
from openswell.services import SwellService, WeatherService, SpotService, GeocodeService, SurfRecommenderService
from openswell.agents import create_surf_recommender_llm


def generate_lifespan(config: Config | None):
    config = config or Config()
    @asynccontextmanager
    async def lifespan(
        app: FastAPI,
    ):
        swell_client = SwellClient(config=config)
        weather_client = WeatherClient(config=config)
        geocode_client = GeocodeClient(config=config)

        swell_service = SwellService(client=swell_client)
        weather_service = WeatherService(client=weather_client)
        geocode_service = GeocodeService(client=geocode_client)
        spot_service = SpotService(config=config)

        surf_recommender_service = SurfRecommenderService(
            swell_service=swell_service,
            weather_service=weather_service,
            spot_service=spot_service,
        )

        # surf_recommender_tool = create_surf_recommendation_tool(
        #     surf_recommender=surf_recommender_service,
        # )


        # surf_recommender_agent = create_surf_recommender_agent(
        #     config=config,
        #     tools=[surf_recommender_tool],
        # )

        surf_recommender_llm = create_surf_recommender_llm(
            config=config
        )

        app.state.config = config
        app.state.geocode_service = geocode_service
        app.state.surf_recommender_service = surf_recommender_service
        app.state.surf_recommender_llm = surf_recommender_llm
        # app.state.surf_recommender_agent = surf_recommender_agent

        yield

        # Cleanup (if needed later)
        # e.g. close clients, DB connections
    
    return lifespan