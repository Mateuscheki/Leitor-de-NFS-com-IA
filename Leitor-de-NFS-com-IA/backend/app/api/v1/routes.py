from fastapi import APIRouter
from app.api.v1.endpoints import notas

api_router = APIRouter()
api_router.include_router(notas.router, prefix="/notas", tags=["Notas Fiscais"])