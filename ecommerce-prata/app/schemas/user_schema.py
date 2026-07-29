from pydantic import BaseModel, EmailStr
from app.enums.order_status import OrderStatus

class OrderResponse(BaseModel):

    status: OrderStatus

class UserCreate(BaseModel):

    name: str

    email: EmailStr

    password: str

class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    is_admin: bool

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str    