from fastapi import APIRouter
from app.features.accidents.router import router as accidents_router

api_router = APIRouter()

# Register the accidents feature
api_router.include_router(accidents_router)