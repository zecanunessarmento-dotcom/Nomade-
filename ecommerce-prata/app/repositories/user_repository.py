from sqlalchemy.orm import Session
from app.models.user import User
from app.models.product import Product

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):

        user = (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

        return user

    def create(self, user: User):

        self.db.add(user)

        self.db.commit()

        self.db.refresh(user)

        return user
    
    def get_by_email(self, email: str):
        return (
        self.db.query(User)
        .filter(User.email == email)
        .first()
    ) 

    def get_by_id(self, user_id: int):
        return (
        self.db.query(User)
        .filter(User.id == user_id)
        .first()
    )
    class ProductRepository:

        def __init__(self, db):
            self.db = db


        def list_all(self):
            return self.db.query(Product).all()