from decimal import Decimal
from typing import Annotated

from pydantic import Field

# ==========================================================
# Texto
# ==========================================================

ProductName = Annotated[
    str,
    Field(
        min_length=2,
        max_length=150
    )
]

Description = Annotated[
    str | None,
    Field(
        max_length=1000
    )
]

# ==========================================================
# Valores monetários
# ==========================================================

PositiveMoney = Annotated[
    Decimal,
    Field(
        gt=Decimal("0.00")
    )
]

# ==========================================================
# Valores inteiros
# ==========================================================

PositiveInt = Annotated[
    int,
    Field(
        ge=0
    )
]