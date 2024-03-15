from abc import abstractmethod

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError("This method is not implemented")


class BaseOrderModel(BaseModel):
    __abstract__ = True
    name = str
    address = str
    type_annotation_map = {
        str: String().with_variant(String(300), "postgresql"),
    }
