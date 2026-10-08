import enum
import uuid
from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserRole(str, enum.Enum):
    admin = 'admin'
    user = 'user'


class User(Base):
    __tablename__ = "users"

    id = Column("user_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole, name="user_role"), default=UserRole.user)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    accidents = relationship("Accident", back_populates="reporter")
    comments = relationship("Comment", back_populates="author")