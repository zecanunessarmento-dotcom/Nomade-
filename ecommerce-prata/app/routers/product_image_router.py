from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
import os
import shutil
import uuid

from app.core.database import get_db
from app.models.product import Product
from app.models.product_image import ProductImage


router = APIRouter(
    prefix="/products",
    tags=["Product Images"],
)


UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/{product_id}/images")
def add_product_image(
    product_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Verifica se o produto existe
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado."
        )

    # Verifica extensão
    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    }

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Formato de imagem inválido. "
                "Use JPG, JPEG, PNG ou WEBP."
            ),
        )

    # Gera nome único
    filename = f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename
    )

    # Salva arquivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    # URL que será salva no banco
    image_url = f"/uploads/{filename}"

    # Cria registro no banco
    image = ProductImage(
        image_url=image_url,
        product_id=product_id,
    )

    db.add(image)
    db.commit()
    db.refresh(image)

    return {
        "id": image.id,
        "product_id": image.product_id,
        "image_url": image.image_url,
    }