from passlib.context import CryptContext
from app.core.config import settings

settings.SECRET_KEY
settings.ALGORITHM
settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    password: str,
    password_hash: str
) -> bool:
    
    return pwd_context.verify(
        password,
        password_hash
    )