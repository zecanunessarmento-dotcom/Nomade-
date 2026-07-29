from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user

from app.models.user import User

from app.services.order_service import OrderService

from app.schemas.order_schema import (
    OrderResponse,
    OrderListResponse
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post(
    "/checkout",
    response_model=OrderResponse
)
def checkout(

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    service = OrderService(db)

    return service.finalize_order(
        current_user.id
    )

@router.get(
    "",
    response_model=list[OrderListResponse]
)
def list_orders(

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    service = OrderService(db)

    return service.list_by_user(
        current_user.id
    )

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(

    order_id: int,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    service = OrderService(db)

    return service.get_by_id(
        order_id,
        current_user.id
    )

@router.patch(
    "/{order_id}/cancel"
)
def cancel_order(

    order_id: int,

    current_user: User = Depends(get_current_user),

    db: Session = Depends(get_db)

):

    service = OrderService(db)

    return service.cancel_order(
        order_id,
        current_user.id
    )