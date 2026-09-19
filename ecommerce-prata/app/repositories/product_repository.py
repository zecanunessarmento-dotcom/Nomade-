from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self, db: Session):
        super().__init__(db, Product)

    def get_by_name(self, name: str) -> Product | None:
        return (
            self.db.query(Product)
            .filter(
                func.lower(Product.name) == name.lower()
            )
            .first()
        )

    def get_by_category(self, category_id: int) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(Product.category_id == category_id)
            .all()
        )

    def search_by_name(self, name: str) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(
                func.lower(Product.name).contains(name.lower())
            )
            .all()
        )

    def increase_stock(
        self,
        product: Product,
        quantity: int
    ) -> Product:
        product.stock += quantity
        self.db.flush()
        return product

    def decrease_stock(
        self,
        product: Product,
        quantity: int
    ) -> Product:
        product.stock -= quantity
        self.db.flush()
        return product