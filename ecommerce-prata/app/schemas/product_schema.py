from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.common import (
    Description,
    PositiveInt,
    PositiveMoney,
    ProductName,
)


class ProductImageResponse(BaseModel):
    id: int
    image_url: str

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: ProductName
    description: Description = None
    price: PositiveMoney
    stock: PositiveInt
    category_id: int

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "O nome do produto é obrigatório."
            )

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return None

        value = value.strip()

        return value or None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: ProductName | None = None
    description: Description = None
    price: PositiveMoney | None = None
    stock: PositiveInt | None = None
    category_id: int | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError(
                "O nome do produto é obrigatório."
            )

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return None

        value = value.strip()

        return value or None


class ProductResponse(ProductBase):
    id: int
    images: list[ProductImageResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )