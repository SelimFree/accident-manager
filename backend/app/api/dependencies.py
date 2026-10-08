from app.core.database import AsyncSessionLocal

async def get_db():
    """Dependency to inject the database session into routes."""
    async with AsyncSessionLocal() as session:
        yield session

# Future dependencies go here:
# async def get_current_user(...):
# async def verify_admin_role(...):