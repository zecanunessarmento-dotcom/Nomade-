from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# ==================================================
# CRIAR PRODUTO
# ==================================================

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)

    return service.create_product(data)


# ==================================================
# LISTAR TODOS OS PRODUTOS
# ==================================================

@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products(
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    return service.get_products()


# ==================================================
# BUSCAR PRODUTO POR NOME
# ==================================================

@router.get(
    "/search",
    response_model=list[ProductResponse],
)
def search_products(
    name: str,
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    return service.search_products(name)


# ==================================================
# LISTAR PRODUTOS POR CATEGORIA
# ==================================================

@router.get(
    "/category/{category_id}",
    response_model=list[ProductResponse],
)
def get_products_by_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    return service.get_products_by_category(category_id)


# ==================================================
# BUSCAR PRODUTO POR ID
# ==================================================

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    service = ProductService(db)

    return service.get_product(product_id)


# ==================================================
# ATUALIZAR PRODUTO
# ==================================================

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)

    return service.update_product(
        product_id=product_id,
        product_data=data,
    )


# ==================================================
# EXCLUIR PRODUTO
# ==================================================

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)

    service.delete_product(product_id)

    return None


# ==================================================
# AUMENTAR ESTOQUE
# ==================================================

@router.patch(
    "/{product_id}/stock/increase",
    response_model=ProductResponse,
)
def increase_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)

    return service.increase_stock(
        product_id=product_id,
        quantity=quantity,
    )


# ==================================================
# DIMINUIR ESTOQUE
# ==================================================

@router.patch(
    "/{product_id}/stock/decrease",
    response_model=ProductResponse,
)
def decrease_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProductService(db)

    return service.decrease_stock(
        product_id=product_id,
        quantity=quantity,
    )