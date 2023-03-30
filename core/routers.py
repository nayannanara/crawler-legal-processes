from fastapi import APIRouter

from core.processes import controller as processes

api_router = APIRouter()

api_router.include_router(
    processes.router, prefix='/processes', tags=['processes']
)
