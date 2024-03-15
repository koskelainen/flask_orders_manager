from sqlalchemy import Column, DateTime, Integer, MetaData, String, func

from src.domain.models import BaseOrderModel


class OrderModel(BaseOrderModel):
    __tablename__ = "orders"
    __table_args__ = {"schema": "public"}
    metadata = MetaData()
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(300), nullable=False)
    address = Column(String(300), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"OrderModel(id={self.id!r}, name={self.name!r}, address={self.address!r})"
