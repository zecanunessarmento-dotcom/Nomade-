from pydantic import BaseModel, Field
from pydantic import BaseModel
from typing import List

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True

class CartResponse(BaseModel):

    id: int

    items: List[CartProductResponse]

    total: float

    class Config:
        from_attributes = True

class CartProductResponse(BaseModel):

    product_id: int

    name: str

    price: float

    image_url: str | None = None

    quantity: int

    subtotal: float

    class Config:
        from_attributes = True