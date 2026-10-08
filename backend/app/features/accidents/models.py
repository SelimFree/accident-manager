import enum
import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.database import Base
from app.features.users.models import User
from app.features.comments.models import Comment

class AccidentStatus(str, enum.Enum):
    pending = 'pending'
    in_progress = 'in_progress'
    resolved = 'resolved'

class Accident(Base):
    __tablename__ = "accidents"

    id = Column("accident_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(AccidentStatus, name="accident_status"), default=AccidentStatus.pending)
    is_deleted = Column(Boolean, default=False)
    location = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    reporter = relationship(User, back_populates="accidents")
    comments = relationship(Comment, back_populates="accident")