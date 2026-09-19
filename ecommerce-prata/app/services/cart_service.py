from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.cart_repository import CartRepository
from app.repositories.product_repository import ProductRepository


class CartService:

    def __init__(self, db: Session):
        self.db = db

        self.cart_repository = CartRepository(db)
        self.product_repository = ProductRepository(db)

    # ==================================================
    # BUSCAR CARRINHO
    # ==================================================

    def get_cart(
        self,
        user_id: int
    ):

        cart = self.cart_repository.get_by_user_id(
            user_id
        )

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )

        return cart

    # ==================================================
    # ADICIONAR ITEM
    # ==================================================

    def add_item(
        self,
        user_id: int,
        product_id: int,
        quantity: int
    ):

        if quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="A quantidade deve ser maior que zero."
            )

        product = self.product_repository.get_by_id(
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )

        if product.stock <= 0:
            raise HTTPException(
                status_code=400,
                detail="Produto sem estoque."
            )

        cart = self.cart_repository.get_or_create_by_user_id(
            user_id
        )

        item = self.cart_repository.get_item(
            cart.id,
            product_id
        )

        if item:

            new_quantity = (
                item.quantity + quantity
            )

            if new_quantity > product.stock:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade solicitada "
                        "superior ao estoque disponível."
                    )
                )

            item.quantity = new_quantity

        else:

            if quantity > product.stock:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Quantidade solicitada "
                        "superior ao estoque disponível."
                    )
                )

            self.cart_repository.create_item(
                cart_id=cart.id,
                product_id=product.id,
                quantity=quantity
            )

        try:

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

        return self.cart_repository.get_by_user_id(
            user_id
        )

    # ==================================================
    # ATUALIZAR QUANTIDADE
    # ==================================================

    def update_quantity(
        self,
        user_id: int,
        product_id: int,
        quantity: int
    ):

        if quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="A quantidade deve ser maior que zero."
            )

        cart = self.cart_repository.get_by_user_id(
            user_id
        )

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )

        item = self.cart_repository.get_item(
            cart.id,
            product_id
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Produto não está no carrinho."
            )

        product = self.product_repository.get_by_id(
            product_id
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado."
            )

        if quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Quantidade solicitada "
                    "superior ao estoque disponível."
                )
            )

        item.quantity = quantity

        try:

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

        return self.cart_repository.get_by_user_id(
            user_id
        )

    # ==================================================
    # REMOVER ITEM
    # ==================================================

    def remove_item(
        self,
        user_id: int,
        product_id: int
    ):

        cart = self.cart_repository.get_by_user_id(
            user_id
        )

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )

        item = self.cart_repository.get_item(
            cart.id,
            product_id
        )

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Produto não está no carrinho."
            )

        try:

            self.cart_repository.delete_item(
                item
            )

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

        return self.cart_repository.get_by_user_id(
            user_id
        )

    # ==================================================
    # LIMPAR CARRINHO
    # ==================================================

    def clear_cart(
        self,
        user_id: int
    ):

        cart = self.cart_repository.get_by_user_id(
            user_id
        )

        if not cart:
            raise HTTPException(
                status_code=404,
                detail="Carrinho não encontrado."
            )

        try:

            self.cart_repository.clear(
                cart
            )

            self.db.commit()

        except Exception:

            self.db.rollback()

            raise

        return {
            "message": "Carrinho limpo com sucesso."
        }