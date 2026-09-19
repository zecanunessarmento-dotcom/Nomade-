from app.core.database import SessionLocal

# Importar os modelos relacionados antes de usar o SQLAlchemy
from app.models.user import User
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category
from app.models.order import Order
from app.models.order_item import OrderItem


db = SessionLocal()

try:
    image = (
        db.query(ProductImage)
        .filter(ProductImage.id == 2)
        .first()
    )

    if image:
        db.delete(image)
        db.commit()
        print("Imagem removida com sucesso.")
    else:
        print("Imagem não encontrada.")

finally:
    db.close()