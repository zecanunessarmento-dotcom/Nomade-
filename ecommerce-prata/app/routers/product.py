from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category
from app.database import get_db
from app.services.product_service import ProductService
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db)
):
    service = ProductService(db)

    products = service.list_products()

    return products

@router.get("/{product_id}",
            response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product

@router.post(
    "/",
    response_model=ProductResponse
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == product.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    new_product = Product(
        **product.model_dump()
    )

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return new_product

@router.put("/{product_id}",
            response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    for key, value in product_data.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Produto removido com sucesso"
    }