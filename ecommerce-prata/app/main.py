from fastapi import FastAPI

from app.core.database import Base, engine

from app.models.user import User
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem
from fastapi.staticfiles import StaticFiles
from app.routers.category_router import router as category_router
from app.routers.product_router import router as product_router
from app.routers.upload import router as upload_router
from app.routers.auth_router import router as auth_router
from app.routers import cart_router
from app.routers.order_router import router as order_router
from app.routers.product_image_router import router as product_image_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce de Joias"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(product_router)
app.include_router(category_router)
app.include_router(upload_router)
app.include_router(product_image_router)
app.include_router(auth_router)
app.include_router(cart_router.router)

@app.get("/")
def home():
    return {
        "message": "API funcionando"
    }