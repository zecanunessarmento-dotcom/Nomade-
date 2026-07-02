from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.models.user import User

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