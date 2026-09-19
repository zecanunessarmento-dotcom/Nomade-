from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


class CartRepository:

    def __init__(self, db: Session):
        self.db = db

    # ==========================================
    # Buscar carrinho pelo usuário
    # ==========================================

    def get_by_user_id(
        self,
        user_id: int
    ) -> Cart | None:

        return (
            self.db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )

    # ==========================================
    # Buscar ou criar carrinho
    # ==========================================

    def get_or_create_by_user_id(
        self,
        user_id: int
    ) -> Cart:

        cart = self.get_by_user_id(user_id)

        if cart:
            return cart

        cart = Cart(
            user_id=user_id
        )

        self.db.add(cart)

        self.db.flush()

        return cart

    # ==========================================
    # Buscar item específico do carrinho
    # ==========================================

    def get_item(
        self,
        cart_id: int,
        product_id: int
    ) -> CartItem | None:

        return (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
            .first()
        )

    # ==========================================
    # Adicionar item ao carrinho
    # ==========================================

    def create_item(
        self,
        cart_id: int,
        product_id: int,
        quantity: int
    ) -> CartItem:

        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )

        self.db.add(cart_item)

        self.db.flush()

        return cart_item

    # ==========================================
    # Buscar todos os itens do carrinho
    # ==========================================

    def get_items(
        self,
        cart_id: int
    ) -> list[CartItem]:

        return (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id
            )
            .all()
        )

    # ==========================================
    # Remover item
    # ==========================================

    def delete_item(
        self,
        item: CartItem
    ) -> None:

        self.db.delete(item)

        self.db.flush()

    # ==========================================
    # Limpar carrinho
    # ==========================================

    def clear(
        self,
        cart: Cart
    ) -> None:

        cart.items.clear()

        self.db.flush()