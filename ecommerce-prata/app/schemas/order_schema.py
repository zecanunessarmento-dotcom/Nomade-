from decimal import Decimal
from pydantic import BaseModel
from datetime import datetime
from app.enums.order_status import OrderStatus

class OrderItemResponse(BaseModel):

    product_id: int

    product_name: str

    quantity: int

    unit_price: Decimal

    subtotal: Decimal

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):

    id: int

    status: OrderStatus

    subtotal: Decimal

    discount: Decimal

    shipping: Decimal

    tax: Decimal

    total: Decimal

    created_at: datetime

    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
    
class OrderListResponse(BaseModel):

    id: int

    status: str

    total: Decimal

    created_at: datetime

    class Config:
        from_attributes = True