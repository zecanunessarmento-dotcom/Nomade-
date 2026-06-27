from sqlalchemy.orm import Session
from app.repositories.product_repository import ProductRepository
from app.models.product import Product


class ProductService:

    def __init__(self, db):
        self.repository = ProductRepository(db)

    def list_products(self):

        products = self.repository.list_all()

        return products