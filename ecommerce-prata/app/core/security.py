from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt

from app.core.config import settings


def _normalize_password(password: str) -> str:
    if not password:
        return password

    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        return password_bytes[:72].decode("utf-8", errors="ignore")

    return password


def hash_password(password: str) -> str:
    normalized_password = _normalize_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(normalized_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    normalized_password = _normalize_password(password)
    return bcrypt.checkpw(
        normalized_password.encode("utf-8"),
        password_hash.encode("utf-8")
    )

def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None