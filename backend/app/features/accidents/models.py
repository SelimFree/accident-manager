import enum
import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, func, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.database import Base


class AccidentStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    resolved = "resolved"


class IncidentCategory(str, enum.Enum):
    accident = "accident"
    road_work = "road_work"
    road_closure = "road_closure"
    pothole = "pothole"
    traffic_light = "traffic_light"
    other = "other"


class IncidentSeverity(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Accident(Base):
    __tablename__ = "accidents"
    __table_args__ = (Index("accident_location_idx", "location", postgresql_using="gist"),)

    id = Column("accident_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(AccidentStatus, name="accident_status"), default=AccidentStatus.pending, nullable=False)
    category = Column(SQLEnum(IncidentCategory, name="incident_category"), default=IncidentCategory.other, nullable=False)
    severity = Column(SQLEnum(IncidentSeverity, name="incident_severity"), default=IncidentSeverity.medium, nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=True)
    ends_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    location = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=False), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reporter = relationship("User", back_populates="accidents", foreign_keys=[reporter_id])
    comments = relationship("Comment", back_populates="accident")