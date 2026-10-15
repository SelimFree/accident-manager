from fastapi import APIRouter
from app.features.auth.router import router as auth_router
from app.features.accidents.router import router as accidents_router
from app.features.admin.router import router as admin_router
from app.features.users.router import router as users_router
from app.features.comments.router import router as comments_router

# Register the accidents feature
api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(accidents_router)
api_router.include_router(admin_router)
api_router.include_router(comments_router)