"""API factory defintion."""
from fastapi import FastAPI
from openswell.api.lifespan import generate_lifespan
from openswell.api.routes import register_routes
from openswell.core.config import Config


def build_api_app(
    config: Config | None = None,
) -> FastAPI:
    """
    Factory function to build FastAPI application, based on configurations.
    """

    config = config or Config()
    lifespan = generate_lifespan(config=config)

    app = FastAPI(
        title="openswell",
        description="Openswell surf recommender agent.",
        version=config.version,
        openapi_url="/common/api-docs",
        lifespan=lifespan,
    )

    register_routes(app=app)

    return app

