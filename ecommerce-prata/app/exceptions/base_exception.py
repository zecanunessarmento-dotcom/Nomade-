class AppException(Exception):
    """
    Exceção base da aplicação.
    """

    status_code = 500
    detail = "Erro interno."

    def __init__(self, detail: str | None = None):
        if detail:
            self.detail = detail