from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

def list_all(self):
    products = self.db.query(Product).all()

    return products