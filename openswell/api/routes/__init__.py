"""Openswell API routes entrypoint."""
from fastapi import FastAPI
from openswell.api.routes.health import router as health_router
from openswell.api.routes.v1 import build_v1_router

def register_routes(app: FastAPI) -> None:
    """
    Register all routes of the API with the FastAPI app.
    
    Args:
        app: the FastAPI application.
        config: the app configuration.
    """
    app.include_router(
        router=health_router,
        prefix="/health",
        tags=["common"]
    )

    app.include_router(router=build_v1_router(), prefix="/api/v1")

__all__ = ["register_routes"]