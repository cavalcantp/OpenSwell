from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_health():
    """Health endpoint."""
    return "Healthy."
