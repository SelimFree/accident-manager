from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.api.dependencies import get_db, get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.features.auth.schemas import RegisterRequest, LoginRequest, UserResponse, TokenResponse
from app.features.users.models import User, UserRole

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    email = str(data.email).lower()
    user = User(name=data.name, email=email, password_hash=hash_password(data.password), role=UserRole.user)
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email is already registered") from exc
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == str(data.email).lower()))
    if not user or not user.is_active or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserResponse)
async def me(user: User = Depends(get_current_user)):
    return user
