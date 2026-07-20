from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order_item import OrderItem


class OrderItemRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        order_id: int,
        product_id: int,
        product_name: str,
        quantity: int,
        unit_price: Decimal,
        subtotal: Decimal
    ) -> OrderItem:

        order_item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )

        self.db.add(order_item)
        self.db.flush()

        return order_item

    def list_by_order(
        self,
        order_id: int
    ) -> list[OrderItem]:

        return (
            self.db.query(OrderItem)
            .filter(OrderItem.order_id == order_id)
            .all()
        )