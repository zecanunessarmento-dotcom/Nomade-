from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    # ==========================================================
    # Campos
    # ==========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False,
        index=True
    )

    description = Column(
        String(1000),
        nullable=True
    )

    price = Column(
        Numeric(10, 2),
        nullable=False
    )

    stock = Column(
        Integer,
        nullable=False
    )

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    # ==========================================================
    # Relacionamentos
    # ==========================================================

    category = relationship(
        "Category",
        back_populates="products"
    )

    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    cart_items = relationship(
        "CartItem",
        back_populates="product"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )