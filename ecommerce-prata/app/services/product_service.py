from sqlalchemy.orm import Session

from app.models.product import Product

from app.repositories.product_repository import ProductRepository
from app.repositories.category_repository import CategoryRepository

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
)

from app.exceptions.category_exceptions import (
    CategoryNotFoundException,
)

from app.exceptions.product_exceptions import (
    InsufficientStockException,
    ProductAlreadyExistsException,
    ProductNotFoundException,
)


class ProductService:
    """
    Camada responsável pelas regras de negócio
    relacionadas aos produtos.
    """

    def __init__(self, db: Session):
        self.db = db

        self.product_repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)

    # =========================================================
    # CRIAR PRODUTO
    # =========================================================

    def create_product(
        self,
        product_data: ProductCreate,
    ) -> Product:

        try:
            # Verifica se a categoria existe
            category = self.category_repository.get_by_id(
                product_data.category_id
            )

            if category is None:
                raise CategoryNotFoundException(
                    product_data.category_id
                )

            # Verifica se já existe produto com o mesmo nome
            existing_product = (
                self.product_repository.get_by_name(
                    product_data.name
                )
            )

            if existing_product is not None:
                raise ProductAlreadyExistsException(
                    product_data.name
                )

            # Cria o produto
            product = Product(
                name=product_data.name,
                description=product_data.description,
                price=product_data.price,
                stock=product_data.stock,
                category_id=product_data.category_id,
            )

            # Persiste através do Repository
            self.product_repository.create(product)

            # Confirma a transação
            self.db.commit()

            # Atualiza o objeto com os dados do banco
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # =========================================================
    # BUSCAR PRODUTO POR ID
    # =========================================================

    def get_product(
        self,
        product_id: int,
    ) -> Product:

        product = self.product_repository.get_by_id(
            product_id
        )

        if product is None:
            raise ProductNotFoundException(
                product_id
            )

        return product

    # =========================================================
    # LISTAR PRODUTOS
    # =========================================================

    def get_products(self) -> list[Product]:

        return self.product_repository.get_all()

    # =========================================================
    # ATUALIZAR PRODUTO
    # =========================================================

    def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate,
    ) -> Product:

        try:
            # Busca o produto
            product = self.get_product(product_id)

            # Pega somente os campos enviados
            update_data = product_data.model_dump(
                exclude_unset=True
            )

            # Verifica alteração de categoria
            if "category_id" in update_data:

                category = (
                    self.category_repository.get_by_id(
                        update_data["category_id"]
                    )
                )

                if category is None:
                    raise CategoryNotFoundException(
                        update_data["category_id"]
                    )

            # Verifica alteração de nome
            if "name" in update_data:

                existing_product = (
                    self.product_repository.get_by_name(
                        update_data["name"]
                    )
                )

                # Não permite usar o nome de outro produto
                if (
                    existing_product is not None
                    and existing_product.id != product_id
                ):
                    raise ProductAlreadyExistsException(
                        update_data["name"]
                    )

            # Atualiza os campos enviados
            for field, value in update_data.items():
                setattr(
                    product,
                    field,
                    value
                )

            # Persiste alteração
            self.product_repository.update(product)

            # Confirma transação
            self.db.commit()

            # Atualiza objeto
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # =========================================================
    # EXCLUIR PRODUTO
    # =========================================================

    def delete_product(self, product_id: int) -> None:
        try:
            product = self.get_product(product_id)

        # Verifica se o produto já foi utilizado em algum pedido
            if product.order_items:
                raise ValueError(
                    "Não é possível excluir este produto porque ele "
                    "já está associado a um ou mais pedidos."
            )

            # Exclui o produto
            self.product_repository.delete(product)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise
    # =========================================================
    # PRODUTOS POR CATEGORIA
    # =========================================================

    def get_products_by_category(
        self,
        category_id: int,
    ) -> list[Product]:

        # Verifica se a categoria existe
        category = self.category_repository.get_by_id(
            category_id
        )

        if category is None:
            raise CategoryNotFoundException(
                category_id
            )

        # Busca produtos da categoria
        return self.product_repository.get_by_category(
            category_id
        )

    # =========================================================
    # PESQUISAR PRODUTOS
    # =========================================================

    def search_products(
        self,
        name: str,
    ) -> list[Product]:

        return self.product_repository.search_by_name(
            name
        )

    # =========================================================
    # AUMENTAR ESTOQUE
    # =========================================================

    def increase_stock(
        self,
        product_id: int,
        quantity: int,
    ) -> Product:

        # Validação da quantidade
        if quantity <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        try:
            # Busca produto
            product = self.get_product(product_id)

            # Aumenta estoque
            self.product_repository.increase_stock(
                product,
                quantity
            )

            # Confirma transação
            self.db.commit()

            # Atualiza objeto
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise

    # =========================================================
    # DIMINUIR ESTOQUE
    # =========================================================

    def decrease_stock(
        self,
        product_id: int,
        quantity: int,
    ) -> Product:

        # Validação da quantidade
        if quantity <= 0:
            raise ValueError(
                "A quantidade deve ser maior que zero."
            )

        try:
            # Busca produto
            product = self.get_product(product_id)

            # Verifica estoque disponível
            if product.stock < quantity:
                raise InsufficientStockException(
                    product_id=product.id,
                    available_stock=product.stock,
                    requested_quantity=quantity,
                )

            # Diminui estoque
            self.product_repository.decrease_stock(
                product,
                quantity
            )

            # Confirma transação
            self.db.commit()

            # Atualiza objeto
            self.db.refresh(product)

            return product

        except Exception:
            self.db.rollback()
            raise