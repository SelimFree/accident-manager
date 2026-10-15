from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import get_settings

hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        return hasher.verify(password, stored_hash)
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: UUID) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> UUID:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "access":
            raise ValueError("Wrong token type")
        return UUID(payload["sub"])
    except (InvalidTokenError, ValueError, KeyError, TypeError) as exc:
        raise ValueError("Invalid access token") from exc
