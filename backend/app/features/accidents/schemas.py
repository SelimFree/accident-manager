from pydantic import BaseModel, Field
from uuid import UUID
from typing import Tuple, Optional
from datetime import datetime
from app.features.accidents.models import AccidentStatus

class AccidentBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: AccidentStatus = AccidentStatus.pending
    coordinates: Tuple[float, float] = Field(..., description="[Latitude, Longitude]")

class AccidentCreate(AccidentBase):
    reporter_id: UUID

class AccidentResponse(AccidentBase):
    id: UUID
    reporter_id: UUID
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True