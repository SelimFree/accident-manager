from datetime import datetime
from typing import Annotated
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from app.features.users.models import UserRole


class NamePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=2, max_length=80, description="Name shown in the user profile")

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value):
        return value.strip() if isinstance(value, str) else value


class RegisterRequest(NamePayload):
    email: Annotated[EmailStr, Field(max_length=200)]
    password: str = Field(min_length=10, max_length=128)


class UpdateNameRequest(NamePayload):
    pass


class LoginRequest(BaseModel):
    email: Annotated[EmailStr, Field(max_length=200)]
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
