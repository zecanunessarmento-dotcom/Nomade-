from fastapi import FastAPI
from app.routers.category_router import (
    router as category_router
)
from app.database import engine
from app.models.product import Base
from app.models.category import Category
from app.routers.product_router import router as product_router
from fastapi.staticfiles import StaticFiles
from app.routers.upload import (
    router as upload_router
)
Base.metadata.create_all(bind=engine)
from app.routers.auth_router import (
    router as auth_router
)

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