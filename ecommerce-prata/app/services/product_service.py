from sqlalchemy.orm import Session

from app.models.product import Product


class ProductService:

    def __init__(self, db: Session):
        self.db = db

def list_products(self):
    products = self.db.query(Product).all()

    return products