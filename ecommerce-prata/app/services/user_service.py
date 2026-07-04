from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.models.user import User
from app.core.security import (
    verify_password,
    create_access_token
)

class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register(self, user_data):

        existing_user = self.repository.get_by_email(
        user_data.email
    )

        if existing_user:
            raise ValueError("E-mail já cadastrado.")

        password_hash = hash_password(
        user_data.password
    )

        user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=password_hash
    )

        return self.repository.create(user)
    
    def login(self, login_data):

        user = self.repository.get_by_email(
        login_data.email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Email ou senha inválidos."
        )

    access_token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }