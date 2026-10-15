"""Admin moderation with a single incident status and strict transitions."""
from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, require_admin
from app.features.accidents import service
from app.features.accidents.models import Accident, AccidentStatus, NotificationEvent
from app.features.accidents.schemas import AccidentResponse, StatusRequest
from app.features.users.models import User

router = APIRouter(prefix="/api/admin/accidents", tags=["Administration"])

ALLOWED_TRANSITIONS = {
    AccidentStatus.pending: {AccidentStatus.approved, AccidentStatus.rejected},
    AccidentStatus.approved: {AccidentStatus.rejected, AccidentStatus.resolved},
    AccidentStatus.rejected: set(),
    AccidentStatus.resolved: set(),
}


@router.get("/", response_model=list[AccidentResponse])
async def queue(db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin),
                status: AccidentStatus = Query(AccidentStatus.pending),
                limit: int = Query(100, ge=1, le=200)):
    return await service.execute_list(db, Accident.is_deleted.is_(False),
                                      Accident.status == status, limit=limit)


@router.patch("/{incident_id}/status", response_model=AccidentResponse)
async def change_status(incident_id: UUID, payload: StatusRequest,
                        db: AsyncSession = Depends(get_db), admin: User = Depends(require_admin)):
    item = await db.scalar(select(Accident).where(Accident.id == incident_id).with_for_update())
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Incident not found")

    requested = AccidentStatus(payload.status)
    if requested not in ALLOWED_TRANSITIONS[item.status]:
        raise HTTPException(status_code=409, detail=f"Cannot change status from {item.status.value} to {requested.value}")

    item.status = requested
    item.reviewed_by = admin.id
    item.reviewed_at = datetime.now(timezone.utc)
    if requested == AccidentStatus.approved:
        item.verification_source = "admin"
        db.add(NotificationEvent(accident_id=item.id, event_type="incident_approved"))
    elif requested == AccidentStatus.rejected:
        item.verification_source = None

    await db.commit()
    return (await service.execute_list(db, Accident.id == incident_id, limit=1))[0]
