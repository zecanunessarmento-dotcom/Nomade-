from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register(self, user_data):
        existing_user = self.repository.get_by_email(
    user_data.email
)    