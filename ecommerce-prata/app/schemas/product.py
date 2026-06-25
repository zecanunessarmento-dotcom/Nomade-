from pydantic import BaseModel
from app.schemas.category import CategoryResponse

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int

class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int

    category_id: int

    class Config:
        from_attributes = True