from enum import Enum


class OrderStatus(str, Enum):

    PENDING = "PENDING"

    PAID = "PAID"

    PROCESSING = "PROCESSING"

    SHIPPED = "SHIPPED"

    DELIVERED = "DELIVERED"

    CANCELLED = "CANCELLED"