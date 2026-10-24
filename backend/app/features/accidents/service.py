from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from geoalchemy2 import Geography
from geoalchemy2.elements import WKTElement
from sqlalchemy import select, func, cast, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.features.accidents.models import Accident, AccidentStatus
from app.features.accidents.schemas import AccidentCreate, AccidentUpdate
from app.features.users.models import User, UserRole


def nearby_expr(lat: float, lng: float, radius_m: float):
    """Compare geographies in metres (not degrees)."""
    point = func.ST_SetSRID(func.ST_MakePoint(lng, lat), 4326)
    return func.ST_DWithin(cast(Accident.location, Geography(geometry_type="POINT", srid=4326)),
                           cast(point, Geography(geometry_type="POINT", srid=4326)), radius_m)


def public_filter():
    return (Accident.is_deleted.is_(False),
            Accident.status == AccidentStatus.approved,
            or_(Accident.ends_at.is_(None), Accident.ends_at >= func.now()))


async def execute_list(db: AsyncSession, *filters, limit=100, offset=0):
    q = (select(Accident, func.ST_Y(Accident.location).label("lat"),
                func.ST_X(Accident.location).label("lng"))
         .where(*filters).order_by(Accident.created_at.desc()).offset(offset).limit(limit))
    records = (await db.execute(q)).all()
    return [as_response(row[0], row.lat, row.lng) for row in records]


def as_response(accident: Accident, lat: float, lng: float):
    return {
        "id": accident.id,
        "reporter_id": accident.reporter_id,
        "title": accident.title,
        "description": accident.description,
        "category": accident.category,
        "severity": accident.severity,
        "status": accident.status,
        "is_deleted": accident.is_deleted,
        "coordinates": [lat, lng],
        "created_at": accident.created_at,
        "updated_at": accident.updated_at,
        "starts_at": accident.starts_at,
        "ends_at": accident.ends_at,
    }


async def get_one(db: AsyncSession, incident_id: UUID, user: User | None = None):
    rows = await execute_list(db, Accident.id == incident_id, Accident.is_deleted.is_(False), limit=1)
    if not rows:
        raise HTTPException(status_code=404, detail="Incident not found")
    item = rows[0]
    if item["status"] not in (AccidentStatus.approved, AccidentStatus.resolved) and (
        user is None or (user.id != item["reporter_id"] and user.role != UserRole.admin)
    ):
        raise HTTPException(status_code=404, detail="Incident not found")
    return item


async def create(db: AsyncSession, payload: AccidentCreate, user: User):
    recent = await db.scalar(select(func.count(Accident.id)).where(
        Accident.reporter_id == user.id,
        Accident.created_at >= datetime.now(timezone.utc) - timedelta(hours=1)))
    if recent >= get_settings().max_reports_per_hour:
        raise HTTPException(status_code=429, detail="Hourly reporting limit reached")
    lat, lng = payload.coordinates
    item = Accident(reporter_id=user.id, title=payload.title, description=payload.description,
                    category=payload.category, severity=payload.severity, starts_at=payload.starts_at,
                    ends_at=payload.ends_at, status=AccidentStatus.pending,
                    location=WKTElement(f"POINT({lng} {lat})", srid=4326))
    db.add(item)
    await db.commit()
    return (await execute_list(db, Accident.id == item.id, limit=1))[0]


async def update_own(db: AsyncSession, incident_id: UUID, patch: AccidentUpdate, user: User):
    item = await db.scalar(select(Accident).where(Accident.id == incident_id).with_for_update())
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Incident not found")
    if item.reporter_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not your incident")
    if item.status != AccidentStatus.pending:
        raise HTTPException(status_code=409, detail="Only pending reports can be edited")
    values = patch.model_dump(exclude_unset=True)
    if not values:
        raise HTTPException(status_code=422, detail="At least one field must be provided")
    if "coordinates" in values:
        coordinates = values.pop("coordinates")
        if coordinates is None:
            raise HTTPException(status_code=422, detail="coordinates cannot be null")
        lat, lng = coordinates
        item.location = WKTElement(f"POINT({lng} {lat})", srid=4326)
    start = values.get("starts_at", item.starts_at)
    end = values.get("ends_at", item.ends_at)
    if start and end and end <= start:
        raise HTTPException(status_code=422, detail="ends_at must be after starts_at")
    for key in ("starts_at", "ends_at"):
        if values.get(key) and values[key].tzinfo is None:
            raise HTTPException(status_code=422, detail="Use timezone-aware ISO 8601 dates")
    for k, v in values.items():
        if k == "title" and v is None:
            raise HTTPException(status_code=422, detail="title cannot be null")
        if k in {"category", "severity"} and v is None:
            raise HTTPException(status_code=422, detail=f"{k} cannot be null")
        setattr(item, k, v)
    
    # We no longer need to reset confirmations when a user updates their pending report
    await db.commit()
    return (await execute_list(db, Accident.id == incident_id, limit=1))[0]


async def soft_delete(db: AsyncSession, incident_id: UUID, user: User):
    item = await db.get(Accident, incident_id)
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Incident not found")
    if item.reporter_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not your incident")
    if user.role != UserRole.admin and item.status != AccidentStatus.pending:
        raise HTTPException(status_code=409, detail="Ask an admin to remove an approved report")
    item.is_deleted = True
    await db.commit()