from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.cart_schema import CartResponse
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.cart_schema import CartItemCreate
from app.services.cart_service import CartService

router = APIRouter(
    prefix="/cart",
    tags=["Carrinho"]
)

@router.post("/items")
def add_item(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = CartService(db)

    return service.add_item(
        user_id=current_user.id,
        product_id=item.product_id,
        quantity=item.quantity
    )

@router.get(
    "",
    response_model=CartResponse
)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    service = CartService(db)

    return service.get_cart(
        current_user.id
    )