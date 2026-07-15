from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem


class CartRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def get_by_user_id(self, user_id: int):

        return (
            self.db.query(Cart)
            .filter(Cart.user_id == user_id)
            .first()
        )
    
    def create(self, user_id: int):

        cart = Cart(
        user_id=user_id
        )

        self.db.add(cart)

        self.db.commit()

        self.db.refresh(cart)

        return cart
    
    def get_item(
        self,
        cart_id: int,
        product_id: int
    ):

        return (
            self.db.query(CartItem)
            .filter(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id
            )
            .first()
        )
    
    def create_item(
        self,
        cart_id: int,
        product_id: int,
        quantity: int
    ):

        item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity
        )

        self.db.add(item)

        self.db.commit()

        self.db.refresh(item)

        return item
    
    def update_quantity(
        self,
        item: CartItem,
        quantity: int
    ):

        item.quantity = quantity

        self.db.commit()

        self.db.refresh(item)

        return item
    
    def remove_item(
        self,
        item: CartItem
    ):

        self.db.delete(item)

        self.db.commit()