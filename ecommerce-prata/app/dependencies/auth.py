from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from fastapi import Depends, HTTPException, status
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido."
        )

    user_id = int(payload["sub"])

    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário não encontrado."
        )

    return user

def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este recurso."
        )
    return current_user