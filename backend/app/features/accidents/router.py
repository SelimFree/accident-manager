from uuid import UUID
from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db, get_current_user, get_optional_user
from app.features.users.models import User
from app.features.accidents.models import Accident, IncidentCategory
from app.features.accidents.schemas import AccidentResponse, AccidentCreate, AccidentUpdate
from app.features.accidents import service

router = APIRouter(prefix="/api/accidents", tags=["Accidents"])

@router.get("/", response_model=list[AccidentResponse])
async def list_public(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
    west: float | None = Query(None, ge=-180, le=180),
    south: float | None = Query(None, ge=-90, le=90),
    east: float | None = Query(None, ge=-180, le=180),
    north: float | None = Query(None, ge=-90, le=90),
):
    filters = list(service.public_filter())
    bounds = (west, south, east, north)
    if any(x is not None for x in bounds):
        if any(x is None for x in bounds) or west >= east or south >= north:
            raise HTTPException(status_code=422, detail="Provide valid west,south,east,north bounds")
        filters.append(func.ST_Intersects(Accident.location, func.ST_MakeEnvelope(west, south, east, north, 4326)))
    return await service.execute_list(db, *filters, limit=limit, offset=offset)


@router.get("/nearby", response_model=list[AccidentResponse])
async def nearby(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius_m: int = Query(500, ge=20, le=10000),
    db: AsyncSession = Depends(get_db),
):
    return await service.execute_list(db, *service.public_filter(), service.nearby_expr(lat, lng, radius_m))


@router.get("/similar", response_model=list[AccidentResponse])
async def similar(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    category: IncidentCategory = Query(...),
    radius_m: int = Query(100, ge=20, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Let React suggest an existing incident instead of creating duplicates."""
    return await service.execute_list(
        db, Accident.is_deleted.is_(False),
        Accident.status.in_(["pending", "approved"]), Accident.category == category,
        (Accident.ends_at.is_(None) | (Accident.ends_at >= func.now())),
        Accident.created_at >= datetime.now(timezone.utc) - timedelta(hours=48),
        service.nearby_expr(lat, lng, radius_m), limit=30)


@router.get("/mine", response_model=list[AccidentResponse])
async def mine(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = Query(100, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return await service.execute_list(db, Accident.reporter_id == user.id,
                                      Accident.is_deleted.is_(False), limit=limit, offset=offset)


@router.get("/{incident_id}", response_model=AccidentResponse)
async def detail(incident_id: UUID, db: AsyncSession = Depends(get_db), user: User | None = Depends(get_optional_user)):
    return await service.get_one(db, incident_id, user)


@router.post("/", response_model=AccidentResponse, status_code=201)
async def create_incident(data: AccidentCreate, db: AsyncSession = Depends(get_db),
                          user: User = Depends(get_current_user)):
    return await service.create(db, data, user)


@router.patch("/{incident_id}", response_model=AccidentResponse)
async def update_incident(incident_id: UUID, data: AccidentUpdate,
                          db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await service.update_own(db, incident_id, data, user)


@router.delete("/{incident_id}", status_code=204)
async def delete_incident(incident_id: UUID, db: AsyncSession = Depends(get_db),
                          user: User = Depends(get_current_user)):
    await service.soft_delete(db, incident_id, user)
    return Response(status_code=204)