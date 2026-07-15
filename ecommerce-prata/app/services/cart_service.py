from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository

class CartService:
    def __init__(self, db: Session):
        self.cart_repository = CartRepository(db)
        self.product_repository = ProductRepository(db)

    def add_item(
        self,
        user_id: int,
        product_id: int,
        quantity: int
    ):
        cart = self.cart_repository.get_by_user_id(user_id)
        if not cart:
            cart = self.cart_repository.create(user_id)

        # Aqui você pode adicionar lógica para inserir o produto no carrinho
        product = self.product_repository.get_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
    )
        
        item = self.cart_repository.get_item(
            cart.id,
            product.id
)

        if item:

            new_quantity = item.quantity + quantity

        if new_quantity > product.stock:

            raise HTTPException(
                status_code=400,
                detail="Estoque insuficiente."
        )

        self.cart_repository.update_quantity(
            item,
            new_quantity
    )
        if not item:

            if quantity > product.stock:

                raise HTTPException(
                    status_code=400,
                    detail="Estoque insuficiente."
                )

        self.cart_repository.create_item(
            cart.id,
            product.id,
            quantity
    )

        self.cart_repository.create_item(
            cart.id,
            product.id,
            quantity
    )