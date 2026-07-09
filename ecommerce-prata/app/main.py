from fastapi import FastAPI
from app.routers.category_router import (
    router as category_router
)
from app.core.database import Base, engine
from app.models.user import User
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.category import Category
from app.routers.product_router import router as product_router
from fastapi.staticfiles import StaticFiles
from app.routers.upload import (
    router as upload_router
)
from app.routers.auth_router import (
    router as auth_router
)

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
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "API funcionando"
    }