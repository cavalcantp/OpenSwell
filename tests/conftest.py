"""Openswell unit test fixtures"""
from typing import Generator
from fastapi.testclient import TestClient
from pytest import fixture
from unittest.mock import AsyncMock
from langchain_core.runnables import Runnable
from openswell.core.config import Config
from openswell.api.factories import build_api
from openswell.services import GeocodeService, SurfRecommenderService
from openswell.api.dependencies import fetch_geocode_service, fetch_surf_recommender_llm, fetch_surf_recommender_service

@fixture
def config() -> Config:
    return Config()

@fixture
def geocoding_service() -> GeocodeService:
    return AsyncMock(spec=GeocodeService)

@fixture
def surf_recommender_llm() -> Runnable:
    return AsyncMock(spec=Runnable)

@fixture
def surf_recommender_service() -> SurfRecommenderService:
    return AsyncMock(spec=SurfRecommenderService)

@fixture
def client(
    config: Config,
    geocoding_service: GeocodeService,
    surf_recommender_llm: Runnable,
    surf_recommender_service: SurfRecommenderService,
) -> Generator[TestClient, None, None]:
    app = build_api(config=config)
    app.dependency_overrides[fetch_geocode_service] = lambda: geocoding_service
    app.dependency_overrides[fetch_surf_recommender_llm] = lambda: surf_recommender_llm
    app.dependency_overrides[fetch_surf_recommender_service] = lambda: surf_recommender_service

    with TestClient(app=app, headers={"Content-Type": "application/json"}) as client:
        yield client