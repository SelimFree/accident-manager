from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.core.security import decode_access_token
from app.features.users.models import User, UserRole

bearer = HTTPBearer(auto_error=False)


async def get_db():
    """Dependency to inject the database session into routes."""
    async with AsyncSessionLocal() as session:
        yield session


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    try:
        user_id = decode_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
    user = await db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid or inactive user")
    return user


async def get_current_user(user: User | None = Depends(get_optional_user)) -> User:
    if user is None:
        raise HTTPException(status_code=401, detail="Login required", headers={"WWW-Authenticate": "Bearer"})
    return user


async def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user
