from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.api.router import api_router
import app.models
from app.api.dependencies import get_db
from app.core.config import get_settings
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

settings = get_settings()
app = FastAPI(title="Accident Manager API", version="0.2.0")
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
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc
    return {"status": "healthy", "database": "connected"}