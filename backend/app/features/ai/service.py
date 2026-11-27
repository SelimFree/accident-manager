import logging
import re

from app.features.ai.client import GeminiClient
from app.features.ai.fallback import get_fallback_advice
from app.features.ai.prompts import build_incident_prompt

logger = logging.getLogger(__name__)

MAX_RESPONSE_WORDS = 50
MAX_RESPONSE_LENGTH = 600

DISCLAIMER = ("Automated safety advice based on an unverified report.")
EMERGENCY_ADVICE = ("If anyone is injured or in immediate danger, call 112.")
FALLBACK_NOTICE = ("Predefined safety recommendation.")


class InvalidAIResponseError(ValueError):
    """Raised when an AI response fails validation."""


def validate_response(text: str) -> str:

    text = " ".join(text.split())

    if not text:
        raise InvalidAIResponseError("Empty AI response.")

    if len(text) > MAX_RESPONSE_LENGTH:
        raise InvalidAIResponseError("Response is too long.")

    if len(text.split()) > MAX_RESPONSE_WORDS:
        raise InvalidAIResponseError("Response exceeds the word limit.")

    if re.search(r"https?://|www\.", text, re.IGNORECASE):
        raise InvalidAIResponseError("Response contains external links.")

    if any(character.isdigit() for character in text):
        raise InvalidAIResponseError("Response contains unexpected numerical information.")

    if any(character in text for character in "<>`"):
        raise InvalidAIResponseError("Response contains unexpected formatting.")

    return text


def format_comment(
    advice: str,
    is_fallback: bool = False,
) -> str:

    sections = [DISCLAIMER]

    if is_fallback:
        sections.append(FALLBACK_NOTICE)

    sections.extend([advice, EMERGENCY_ADVICE])

    return "\n\n".join(sections)


class AIResponderService:

    def __init__(self, client: GeminiClient):
        self.client = client

    async def generate_comment(
        self,
        category: str,
        severity: str,
    ) -> str:

        prompt = build_incident_prompt( category=category, severity=severity)

        try:
            response = await self.client.generate(prompt)
            advice = validate_response(response)

        except Exception as exc:
            logger.warning(
                "AI generation failed (%s). "
                "Using fallback safety advice. "
                "Category: %s, severity: %s",
                type(exc).__name__,
                category,
                severity,
            )

            advice = get_fallback_advice(category=category, severity=severity)

            return format_comment(advice=advice, is_fallback=True)

        return format_comment(advice=advice)