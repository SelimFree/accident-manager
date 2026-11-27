import secrets
from uuid import UUID, NAMESPACE_URL, uuid5

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import hash_password
from app.features.users.models import User, UserRole


SYSTEM_USER_NAME = "AI Safety Assistant"
SYSTEM_USER_EMAIL = "ai.assistant@example.com"

SYSTEM_USER_ID = uuid5(
    NAMESPACE_URL,
    "accident-manager/system/ai-safety-assistant"
)


async def ensure_system_user(db: AsyncSession) -> UUID:
    """Create the system account if it does not already exist."""

    table = User.__table__

    query = select(table).where(
        table.c.user_id == SYSTEM_USER_ID
    )

    result = await db.execute(query)
    user = result.mappings().one_or_none()

    if user is None:
        statement = insert(table).values(
            user_id=SYSTEM_USER_ID,
            name=SYSTEM_USER_NAME,
            email=SYSTEM_USER_EMAIL,
            password_hash=hash_password(
                secrets.token_urlsafe(48)
            ),
            role=UserRole.user,
            is_active=False
        ).on_conflict_do_nothing()

        await db.execute(statement)

        result = await db.execute(query)
        user = result.mappings().one_or_none()

    if (
        user is None
        or user["email"] != SYSTEM_USER_EMAIL
        or user["name"] != SYSTEM_USER_NAME
        or user["role"] != UserRole.user
        or user["is_active"] is not False
    ):
        raise RuntimeError( "AI system account is missing or has an invalid configuration.")

    return SYSTEM_USER_ID


async def provision_system_user() -> UUID:
    """Provision the system account in an independent transaction."""

    async with AsyncSessionLocal.begin() as db:
        return await ensure_system_user(db)
