from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.router import api_router
from app.api.dependencies import get_db
from app.core.config import get_settings
from app.core.database import AsyncSessionLocal
from app.features.users.models import User
from app.core.security import hash_password

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.password_hash == "NEEDS_HASHING"))
        unhashed_users = result.scalars().all()
        
        for user in unhashed_users:
            user.password_hash = hash_password("Password2026!")
            
        if unhashed_users:
            await db.commit()
            print(f"Secured {len(unhashed_users)} seed accounts on startup.")
            
    yield

app = FastAPI(title="Accident Manager API", version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(api_router)

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.scalar(select(1))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"status": "healthy", "database": "connected"}