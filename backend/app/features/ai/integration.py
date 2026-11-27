import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.features.ai.client import GeminiClient
from app.features.ai.fallback import get_fallback_advice
from app.features.ai.service import (
    AIResponderService,
    format_comment,
)
from app.features.ai.system_user import ensure_system_user
from app.features.comments.models import Comment


logger = logging.getLogger(__name__)


async def generate_safety_comment(
    category: str,
    severity: str,
) -> str:

    settings = get_settings()

    api_key = (
        settings.gemini_api_key.get_secret_value()
        if settings.gemini_api_key
        else ""
    )

    if not api_key.strip() or api_key == "YOUR_API_KEY":
        logger.warning("Gemini API key is missing. Using fallback advice.")

        return format_comment(
            advice=get_fallback_advice(category, severity),
            is_fallback=True,
        )

    client = GeminiClient(
        api_key=api_key,
        model=settings.gemini_model,
        timeout_seconds=settings.ai_timeout_seconds,
    )

    service = AIResponderService(client)

    return await service.generate_comment(
        category=category,
        severity=severity,
    )


async def add_automatic_comment(
    db: AsyncSession,
    incident_id: UUID,
    category: str,
    severity: str,
) -> bool:

    try:
        content = await generate_safety_comment(
            category=category,
            severity=severity,
        )

        async with db.begin_nested():
            author_id = await ensure_system_user(db)

            comment = Comment(
                author_id=author_id,
                accident_id=incident_id,
                content=content,
            )

            db.add(comment)
            await db.flush()

        logger.info("Automatic safety comment prepared for incident %s.", incident_id)

        return True

    except Exception as exc:
        logger.error("Automatic comment creation failed for incident %s (%s).", incident_id, type(exc).__name__)

        return False