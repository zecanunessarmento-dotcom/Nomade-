from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class CategoryCreate(BaseModel):
    name: str
    description: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str