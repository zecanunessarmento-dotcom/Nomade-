from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        status: str,
        subtotal: Decimal,
        discount: Decimal,
        shipping: Decimal,
        tax: Decimal,
        total: Decimal
    ) -> Order:

        order = Order(
            user_id=user_id,
            status=status,
            subtotal=subtotal,
            discount=discount,
            shipping=shipping,
            tax=tax,
            total=total
        )

        self.db.add(order)
        self.db.flush()
        self.db.refresh(order)

        return order

    def get_by_id(
        self,
        order_id: int
    ) -> Order | None:

        return (
            self.db.query(Order)
            .filter(Order.id == order_id)
            .first()
        )

    def list_by_user(
        self,
        user_id: int
    ) -> list[Order]:

        return (
            self.db.query(Order)
            .filter(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def update_status(
        self,
        order: Order,
        status: str
    ) -> Order:

        order.status = status

        self.db.flush()

        return order