"""Factory method of OpenSwell API v1 routes."""
from fastapi import APIRouter
from openswell.api.routes.v1.endpoints import chat

def build_router() -> APIRouter:
    """Build API v1 router."""
    router = APIRouter()
    router.include_router(router=chat.router, prefix="/chat")

    return router