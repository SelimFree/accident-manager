import enum
import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, func, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.database import Base


class AccidentStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    resolved = "resolved"


class Accident(Base):
    __tablename__ = "accidents"
    __table_args__ = (Index("accident_location_idx", "location", postgresql_using="gist"),)

    id = Column("accident_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(AccidentStatus, name="accident_status"), default=AccidentStatus.pending, nullable=False)
    category = Column(String(32), nullable=False, default="other")
    severity = Column(String(16), nullable=False, default="medium")
    verification_source = Column(String(16), nullable=True)
    reviewed_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    starts_at = Column(DateTime(timezone=True), nullable=True)
    ends_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    location = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=False), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reporter = relationship("User", back_populates="accidents", foreign_keys=[reporter_id])
    confirmations = relationship("IncidentConfirmation", back_populates="accident", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="accident")


class IncidentConfirmation(Base):
    __tablename__ = "incident_confirmations"
    __table_args__ = (UniqueConstraint("accident_id", "user_id", name="one_confirmation_per_user"),)

    id = Column("confirmation_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accident_id = Column(UUID(as_uuid=True), ForeignKey("accidents.accident_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    accident = relationship("Accident", back_populates="confirmations")
    user = relationship("User", back_populates="confirmations")


class NotificationEvent(Base):
    """Transactional outbox: the future push worker can deliver these events."""
    __tablename__ = "notification_events"

    id = Column("event_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    accident_id = Column(UUID(as_uuid=True), ForeignKey("accidents.accident_id"), nullable=False)
    event_type = Column(String(32), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
