from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, field_validator, model_validator
from app.features.accidents.models import AccidentStatus

Category = Literal["accident", "road_work", "road_closure", "pothole", "traffic_light", "other"]
Severity = Literal["low", "medium", "high"]


def validate_coordinates(value):
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError("coordinates must be [latitude, longitude]")
    lat, lng = value
    if isinstance(lat, bool) or isinstance(lng, bool) or not all(isinstance(x, (float, int)) for x in (lat, lng)):
        raise ValueError("coordinates must be numeric")
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise ValueError("coordinates out of range")
    return (lat, lng)

Coordinates = Annotated[tuple[float, float], BeforeValidator(validate_coordinates)]


class AccidentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=5, max_length=160)
    description: str | None = Field(default=None, max_length=2000)
    category: Category = "other"
    severity: Severity = "medium"
    coordinates: Coordinates = Field(description="[latitude, longitude], WGS84")
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise ValueError("title must contain at least 5 characters")
        return value

    @model_validator(mode="after")
    def dates_consistent(self):
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValueError("ends_at must be after starts_at")
        for dt in (self.starts_at, self.ends_at):
            if dt and dt.tzinfo is None:
                raise ValueError("Use timezone-aware ISO 8601 dates")
        return self


class AccidentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str | None = Field(default=None, min_length=5, max_length=160)
    description: str | None = Field(default=None, max_length=2000)
    category: Category | None = None
    severity: Severity | None = None
    coordinates: Coordinates | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, value: str | None) -> str | None:
        if value is not None and len(value.strip()) < 5:
            raise ValueError("title must contain at least 5 characters")
        return value.strip() if value is not None else None


class AccidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    reporter_id: UUID
    title: str
    description: str | None
    category: Category
    severity: Severity
    status: AccidentStatus
    verification_source: str | None
    confirmations_count: int
    required_confirmations: int
    is_deleted: bool
    coordinates: Coordinates
    starts_at: datetime | None
    ends_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ConfirmationCreate(BaseModel):
    coordinates: Coordinates = Field(description="Current GPS [latitude, longitude]")


class StatusRequest(BaseModel):
    """Admin-only transitions: approval/rejection/resolution; pending is creation-only."""
    model_config = ConfigDict(extra="forbid")
    status: Literal["approved", "rejected", "resolved"]
