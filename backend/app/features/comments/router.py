from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db, get_optional_user
from app.features.comments import service
from app.features.comments.schemas import CommentCreate, CommentUpdate, CommentResponse
from app.features.users.models import User

router = APIRouter(tags=["Comments"])


@router.get("/api/accidents/{incident_id}/comments", response_model=list[CommentResponse])
async def list_comments(
    incident_id: UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    return await service.list_comments(db, incident_id, user, limit, offset)


@router.post("/api/accidents/{incident_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    incident_id: UUID, data: CommentCreate,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user),
):
    return await service.create_comment(db, incident_id, data.content, user)


@router.get("/api/comments/{comment_id}", response_model=CommentResponse)
async def get_comment(
    comment_id: UUID, db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    return await service.get_comment(db, comment_id, user)


@router.patch("/api/comments/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: UUID, data: CommentUpdate,
    db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user),
):
    return await service.update_comment(db, comment_id, data.content, user)


@router.delete("/api/comments/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: UUID, db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    await service.delete_comment(db, comment_id, user)
    return Response(status_code=204)
