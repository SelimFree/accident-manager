from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.features.auth.schemas import UpdateNameRequest, UserResponse
from app.features.users.models import User

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.patch("/me", response_model=UserResponse)
async def update_my_name(
    payload: UpdateNameRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    user.name = payload.name
    await db.commit()
    await db.refresh(user)
    return user
