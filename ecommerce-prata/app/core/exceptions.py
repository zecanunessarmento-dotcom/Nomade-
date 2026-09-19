from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.product_exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException,
    InsufficientStockException,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos os handlers globais de exceções da aplicação.
    """

    @app.exception_handler(ProductNotFoundException)
    async def product_not_found_handler(
        request: Request,
        exc: ProductNotFoundException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "detail": str(exc)
            },
        )

    @app.exception_handler(ProductAlreadyExistsException)
    async def product_already_exists_handler(
        request: Request,
        exc: ProductAlreadyExistsException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "detail": str(exc)
            },
        )

    @app.exception_handler(InsufficientStockException)
    async def insufficient_stock_handler(
        request: Request,
        exc: InsufficientStockException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "detail": str(exc)
            },
        )