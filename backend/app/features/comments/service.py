from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.accidents.models import Accident, AccidentStatus
from app.features.accidents import service as accidents_service
from app.features.comments.models import Comment
from app.features.users.models import User, UserRole


def to_response(comment: Comment, author_name: str) -> dict:
    return {
        "id": comment.id,
        "accident_id": comment.accident_id,
        "author_id": comment.author_id,
        "author_name": author_name,
        "content": comment.content,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
    }


async def get_comment(db: AsyncSession, comment_id: UUID, viewer: User | None = None) -> dict:
    row = (await db.execute(
        select(Comment, User.name)
        .join(User, Comment.author_id == User.id)
        .where(Comment.id == comment_id, Comment.is_deleted.is_(False))
    )).one_or_none()
    if row is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    await accidents_service.get_one(db, row[0].accident_id, viewer)
    return to_response(row[0], row[1])


async def list_comments(db: AsyncSession, incident_id: UUID, viewer: User | None,
                        limit: int, offset: int) -> list[dict]:
    await accidents_service.get_one(db, incident_id, viewer)
    rows = (await db.execute(
        select(Comment, User.name)
        .join(User, Comment.author_id == User.id)
        .where(Comment.accident_id == incident_id, Comment.is_deleted.is_(False))
        .order_by(Comment.created_at.asc(), Comment.id.asc())
        .offset(offset).limit(limit)
    )).all()
    return [to_response(comment, name) for comment, name in rows]


async def create_comment(db: AsyncSession, incident_id: UUID, content: str, user: User) -> dict:
    incident = await db.get(Accident, incident_id)
    if incident is None or incident.is_deleted or incident.status not in (AccidentStatus.approved, AccidentStatus.resolved):
        raise HTTPException(status_code=404, detail="Incident not found")
    if (incident.status == AccidentStatus.resolved or
            (incident.ends_at is not None and incident.ends_at < datetime.now(timezone.utc))):
        raise HTTPException(status_code=409, detail="Comments are closed for this incident")

    item = Comment(author_id=user.id, accident_id=incident_id, content=content)
    db.add(item)
    await db.flush()
    comment_id = item.id
    await db.commit()
    return await get_comment(db, comment_id, user)


async def update_comment(db: AsyncSession, comment_id: UUID, content: str, user: User) -> dict:
    item = await db.get(Comment, comment_id)
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    if item.author_id != user.id:
        raise HTTPException(status_code=403, detail="Only the author can edit this comment")
    await accidents_service.get_one(db, item.accident_id, user)
    item.content = content
    await db.commit()
    return await get_comment(db, comment_id, user)


async def delete_comment(db: AsyncSession, comment_id: UUID, user: User) -> None:
    item = await db.get(Comment, comment_id)
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Comment not found")
    if item.author_id != user.id and user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")
    item.is_deleted = True
    await db.commit()
