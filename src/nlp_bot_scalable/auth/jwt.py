from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from nlp_bot_scalable.config.settings import settings


def create_access_token(user_id: int, email: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError:
        return None
