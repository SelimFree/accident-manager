from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.features.accidents import service
from app.features.accidents.schemas import AccidentResponse, AccidentCreate

router = APIRouter(prefix="/api/accidents", tags=["Accidents"])

@router.get("/", response_model=list[AccidentResponse])
async def get_all_accidents(db: AsyncSession = Depends(get_db)):
    return await service.get_all_accidents(db)

@router.post("/", response_model=AccidentResponse, status_code=201)
async def create_accident(
    accident_in: AccidentCreate, 
    db: AsyncSession = Depends(get_db)
):
    return await service.create_accident(db, accident_in)