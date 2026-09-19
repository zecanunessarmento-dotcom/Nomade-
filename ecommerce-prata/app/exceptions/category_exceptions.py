class CategoryException(Exception):
    """
    Exceção base para erros relacionados a categorias.
    """

    pass


class CategoryNotFoundException(CategoryException):
    """
    Exceção lançada quando uma categoria não é encontrada.
    """

    def __init__(self, category_id: int):
        self.category_id = category_id

        super().__init__(
            f"Categoria com ID {category_id} não encontrada."
        )