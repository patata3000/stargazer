from fastapi import APIRouter

from app.api.api_v1.endpoints import stargazer

api_router = APIRouter()
api_router.include_router(
    stargazer.router,
    prefix="/repos",
    tags=["repos"],
)
