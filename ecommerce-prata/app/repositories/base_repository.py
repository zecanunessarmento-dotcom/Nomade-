from typing import Generic, Type, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Repository base com operações CRUD genéricas.

    Todas as operações utilizam flush() e nunca commit(),
    deixando o controle da transação para a camada de Service.
    """

    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get_by_id(self, entity_id: int) -> ModelType | None:
        return (
            self.db.query(self.model)
            .filter(self.model.id == entity_id)
            .first()
        )

    def get_all(self) -> list[ModelType]:
        return (
            self.db.query(self.model)
            .all()
        )

    def create(self, entity: ModelType) -> ModelType:
        self.db.add(entity)
        self.db.flush()
        return entity

    def update(self, entity: ModelType) -> ModelType:
        self.db.flush()
        return entity

    def delete(self, entity: ModelType) -> None:
        self.db.delete(entity)
        self.db.flush()