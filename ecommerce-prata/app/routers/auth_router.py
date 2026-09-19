from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schema import LoginRequest, TokenResponse
from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserResponse
)

from app.services.user_service import (
    UserService
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)

    try:
        return service.register(user_data)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    login_data = LoginRequest(
        email=form_data.username,
        password=form_data.password
    )

    service = UserService(db)

    return service.login(login_data)

@router.get(
    "/me",
    response_model=UserResponse
)
def me(
    current_user: User = Depends(get_current_user)
):
    return current_user