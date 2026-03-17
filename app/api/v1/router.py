from fastapi import APIRouter
from app.api.v1.endpoints import crypto, health

api_router = APIRouter()

api_router.include_router(
    health.router,
    tags=["Health"],
)

api_router.include_router(
    crypto.router,
    prefix="/crypto",
    tags=["Crypto"],
)