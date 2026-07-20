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