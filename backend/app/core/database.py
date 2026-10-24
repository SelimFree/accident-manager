from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import get_settings

engine = create_async_engine(get_settings().database_url, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()