from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models import BaseOrderModel


class OrdersBasicORM(ABC):
    @abstractmethod
    def create_order(self, order: BaseOrderModel) -> None:
        raise NotImplementedError("This method is not implemented")

    @abstractmethod
    def get_order(self, order_id: int) -> BaseOrderModel:
        raise NotImplementedError("This method is not implemented")

    @abstractmethod
    def update_order(self, order: BaseOrderModel) -> BaseOrderModel:
        raise NotImplementedError("This method is not implemented")

    @abstractmethod
    def delete_order(self, order: BaseOrderModel) -> None:
        raise NotImplementedError("This method is not implemented")

    @abstractmethod
    def search_orders(self, start_id: Optional[int] = None, end_id: Optional[int] = None) -> List[BaseOrderModel]:
        raise NotImplementedError("This method is not implemented")
