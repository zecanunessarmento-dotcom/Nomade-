class ProductException(Exception):
    """
    Exceção base para erros relacionados a produtos.
    """

    pass


class ProductNotFoundException(ProductException):
    """
    Exceção lançada quando um produto não é encontrado.
    """

    def __init__(
        self,
        product_id: int
    ):
        self.product_id = product_id

        super().__init__(
            f"Produto com ID {product_id} não encontrado."
        )


class ProductAlreadyExistsException(ProductException):
    """
    Exceção lançada quando um produto já existe.
    """

    def __init__(
        self,
        product_name: str
    ):
        self.product_name = product_name

        super().__init__(
            f"O produto '{product_name}' já está cadastrado."
        )


class InsufficientStockException(ProductException):
    """
    Exceção lançada quando não há estoque suficiente.
    """

    def __init__(
        self,
        product_id: int,
        available_stock: int,
        requested_quantity: int
    ):
        self.product_id = product_id
        self.available_stock = available_stock
        self.requested_quantity = requested_quantity

        super().__init__(
            f"Estoque insuficiente para o produto "
            f"{product_id}. "
            f"Disponível: {available_stock}. "
            f"Solicitado: {requested_quantity}."
        )