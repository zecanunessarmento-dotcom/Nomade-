from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Numeric,
    String
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    status = Column(
        String,
        nullable=False,
        default="PENDING"
    )

    total = Column(
        Numeric(10, 2),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

subtotal = Column(Numeric(10, 2), nullable=False)

discount = Column(
    Numeric(10, 2),
    nullable=False,
    default=0
)

shipping = Column(
    Numeric(10, 2),
    nullable=False,
    default=0
)

tax = Column(
    Numeric(10, 2),
    nullable=False,
    default=0
)

total = Column(
    Numeric(10, 2),
    nullable=False
)