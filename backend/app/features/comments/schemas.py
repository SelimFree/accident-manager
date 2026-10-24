"""Public comment contracts: never expose a user's email or password hash."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    content: str = Field(min_length=1, max_length=2000)

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Comment cannot be empty")
        return value


class CommentUpdate(CommentCreate):
    """Editing changes the content only, not author/incident/deletion flags."""


class CommentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    accident_id: UUID
    author_id: UUID
    author_name: str
    content: str
    created_at: datetime
    updated_at: datetime